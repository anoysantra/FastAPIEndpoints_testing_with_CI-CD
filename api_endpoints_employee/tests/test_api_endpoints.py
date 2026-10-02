import logging
from playwright.sync_api._generated import APIResponse
import pytest
from playwright.sync_api import APIRequestContext, expect, sync_playwright
from jsonschema import validate
from config import API_ENDPOINT
import random

logger = logging.getLogger(__name__)

# ... (your fixture code here or in conftest.py) ...

EMPLOYEE_SCHEMA = {
    "type": "object",
    "properties": {
        "employee_id": {"type": "string"},
        "name": {"type": "string"},
        "department": {"type": "string"},
        "salary": {"type": "number"},
        "email": {"type": "string", "format": "email"},  # Optional: enforces email format
        "address": {"type": "string"},
    },
    "required": [
        "employee_id",
        "name",
        "department",
        "salary",
        "email",
        "address",
    ],
    "additionalProperties": False,  # Ensures no extra unexpected fields are returned
}


def test_home_endpoint(auth_api_context: APIRequestContext):
    """Verify the API root endpoint responds successfully."""

    logger.info("Checking the API root endpoint")
    response: APIResponse = auth_api_context.get(API_ENDPOINT)
    logger.debug("API root response received with status %s", response.status)
    expect(response).to_be_ok()


def test_create_employee(auth_api_context: APIRequestContext):
    """Create an employee and validate the returned employee data."""
    # Reset EMP_ID for this test

    logger.info("Starting employee creation test")
    # Assign the generated EMP_ID to the payload
    new_emp_id = f"EMP{random.randint(1000, 9999)}"
    employee_payload = {
        "employee_id": new_emp_id,
        "name": "Ananya Roy",
        "department": "QA",
        "salary": 85000,
        "email": f"ananya.{new_emp_id}@example.com",
        "address": "456 TX 78701"
    }
    logger.debug("Creating employee with ID %s", new_emp_id)
    response = auth_api_context.post(url=f"{API_ENDPOINT}/employees", data=employee_payload)
    response_api = response.json()
    logger.info("Employee creation response status: %s", response.status)
    status_code = response_api["status_code"]
    message = response_api["message"]
    assert status_code == 201, f"The status code failed it is: {status_code}"
    assert message == "Employee created successfully", f"Wrong Message"
    validate(instance=response_api["data"], schema=EMPLOYEE_SCHEMA)
    logger.info("Employee response schema validation passed")

    # Optional: If you want to clean up this specific test's entry immediately
    auth_api_context.delete(url=f"{API_ENDPOINT}/employees/{new_emp_id}")
    logger.info("Deletion request completed for employee %s", new_emp_id)



def test_get_all_employees(auth_api_context: APIRequestContext):
    """Verify the endpoint returns the employee collection successfully."""

    logger.info("Fetching all employees")
    response: APIResponse = auth_api_context.get(
        f"{API_ENDPOINT}/employees"
    )
    response_api = response.json()
    logger.debug("Employee collection response status: %s", response.status)
    status_code = response_api.get("status_code")
    assert status_code == 200, f"The status code failed it is: {status_code}"
    message = response_api.get("message")
    assert message == "Employees fetched successfully", f"Wrong api message : {message}"


def test_get_specific_employee(auth_api_context: APIRequestContext):
    """Verify the endpoint returns the requested employee by ID."""
    logger.info("Fetching employee %s", "EMP043")
    get_emp_id = "EMP043"  # Replace with a valid employee ID for testing
    response_api = auth_api_context.get(
        url=f"{API_ENDPOINT}/employees/{get_emp_id}"
    )
    response = response_api.json()
    status_code, message, e_id = (
        response["status_code"],
        response["message"],
        response["data"]["employee_id"],
    )
    assert (
        status_code == 200
    ), f"Employee Data not fetched successfully got the status code : {status_code}"
    assert message == "Employee fetched successfully", "ERROR : Not got success message"
    #assert e_id == emp_id, "Wrong Emp id fetched"


def test_update_employee_data(auth_api_context: APIRequestContext, new_employee: dict):
    """Update an employee and validate the returned employee data."""

    logger.info("Starting employee update test")
    updated_payload = new_employee.copy()
    emp_id = updated_payload["employee_id"]

    employee_data_updated = {
        "employee_id": emp_id,
        "name": "Ananya Roy",
        "department":  "New Department",
        "salary": 55000,
        "email": f"ananya.{emp_id}updated@example.com",
        "address": "Updated Address"
    }

    response_api = auth_api_context.put(
        url=f"{API_ENDPOINT}/employees/{emp_id}", data=employee_data_updated
    )
    response = response_api.json()
    logger.info("Employee update response status: %s", response_api.status)
    status_code, message,department, address = (
        response["status_code"],
        response["message"],
        response["data"]["department"],
        response["data"]["address"],
    )
    assert (
        status_code == 200
    ), f"Employee Data not updated successfully got the status code : {status_code}"
    assert message == "Employee updated successfully", "ERROR : Not got success message"
    assert department == "New Department", "ERROR : Department not updated"
    assert address == "Updated Address", "ERROR : Address not updated"
    validate(instance=response["data"], schema=EMPLOYEE_SCHEMA)
    logger.info("Updated employee response schema validation passed")


def test_delete_employee(auth_api_context: APIRequestContext, new_employee: dict):
    """Verify the endpoint deletes the requested employee successfully."""

    logger.info("Starting employee deletion test")
    employee_payload = new_employee.copy()
    emp_id = employee_payload["employee_id"]
    response_api = auth_api_context.delete(
        url=f"{API_ENDPOINT}/employees/{emp_id}"
    )
    response = response_api.json()
    logger.info("Employee deletion response status: %s", response_api.status)
    assert response["status_code"] == 200, (
        "Employee Data not deleted successfully got the status code : "
        f"{response['status_code']}"
    )
    assert response["message"] == "Employee deleted successfully", (
        "ERROR : Not got deletion success message"
    )

#command to run : pytest -v --log-cli-level=DEBUG
