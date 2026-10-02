import pytest
from playwright.sync_api import sync_playwright, expect, APIRequestContext
from typing import Generator
from json_helper import load_json_data

API_ENDPOINT = "http://127.0.0.1:8000"

@pytest.fixture(scope="session")
def auth_api_context() -> Generator[APIRequestContext, None, None]:
    with sync_playwright() as p:
        request_context : APIRequestContext = p.request.new_context()
        headers = {'Content-Type': 'application/json'}
        creds = load_json_data('data.json')
        credentials = creds["auth_credentials"]
        response = request_context.post(url = f'{API_ENDPOINT}/login', data = credentials, headers = headers)
        response_data = response.json()
        print("Response Data : ",response_data)
        token = response_data.get("access_token")
        request_context.dispose()

        if not token:
            raise RuntimeError(f" the response code is : {response_data.status}❌ No token found in login response")

        api_auth_context = p.request.new_context(
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )

        yield api_auth_context
        api_auth_context.dispose()
        print("Closing")





        
    

        

        
        

 
