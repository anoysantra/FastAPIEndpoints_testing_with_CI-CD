import logging
import pytest
from playwright.sync_api import sync_playwright, expect, APIRequestContext
from typing import Generator
from json_helper import load_json_data
from config import API_ENDPOINT
import random

logger = logging.getLogger(__name__)
#USE THE PYTEST-HOOK : pytest_sessionstarts and along with it levarage storage_state of playwright to bypass login[Complex Integration]
@pytest.fixture(scope="function")
def auth_api_context() -> Generator[APIRequestContext, None, None]:
    with sync_playwright() as p:
        request_context : APIRequestContext = p.request.new_context()
        headers = {'Content-Type': 'application/json'}
        creds = load_json_data('data.json')
        credentials = creds["auth_credentials"]
        logger.info("Authenticating test API client")
        logger.info("Requesting login endpoint: %s", f'{API_ENDPOINT}/login')
        response = request_context.post(url = f'{API_ENDPOINT}/login', data = credentials, headers = headers)
        response_data = response.json()
        token = response_data.get("access_token")
        logger.info("Login response received with status %s", response.status)
        request_context.dispose()

        if not token:
            logger.critical("Login failed; no access token returned (status=%s)", response.status)
            raise RuntimeError(f"Login failed with status {response.status}: no token found")
        logger.info("Login successful; access token obtained")
        api_auth_context = p.request.new_context(
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )
        #request_context.dispose()  # Dispose of the initial request context after obtaining the token
        logger.debug("Yielding authenticated API context for test execution")
        yield api_auth_context
        api_auth_context.dispose()
        logger.debug("Authenticated API context closed")


@pytest.fixture(scope="function")
def new_employee(auth_api_context: APIRequestContext):
    """Dynamically creates a unique employee and cleans it up after the test completes."""

    # 1. SETUP: Create the dynamic data
    emp_id = f"EMP{random.randint(1000, 9999)}"
    employee_data = {
        "employee_id": emp_id,
        "name": "Ananya Roy",
        "department": "QA",
        "salary": 85000,
        "email": "ananya12roy@example.com",
        "address": "456 TX 78701"
    }

    # 2. EXECUTE SETUP: Create the employee in the database
    # (Ensure you fixed the trailing slash issue based on your Swagger spec)
    try:
        response = auth_api_context.post(url=f"{API_ENDPOINT}/employees", data=employee_data)
        if not response.ok:
            raise RuntimeError(f"Failed to create employee {emp_id}. Status code: {response.status}")
    except Exception as e:
        logger.exception("[Setup] Exception occurred while creating employee %s", emp_id)

    # 3. HANDOFF: Pause here and pass data to the test function
    yield employee_data

    # 4. TEARDOWN: This runs automatically AFTER the test function finishes
    logger.info("[Teardown] Cleaning up employee %s", emp_id)

    # Call your API's delete endpoint to wipe the data
    # Adjust the URL format based on your Swagger documentation (e.g., query param or path param)
    try:
        delete_response = auth_api_context.delete(url=f"{API_ENDPOINT}/employees{emp_id}")
        if delete_response.ok:
            logger.info("[Teardown] Successfully deleted employee %s", emp_id)
        else:
            logger.warning(
                "[Teardown] Failed to delete employee %s (status=%s)",
                emp_id,
                delete_response.status,
            )
    except Exception as e:
        logger.exception("[Teardown] Exception occurred while deleting employee %s", emp_id)
