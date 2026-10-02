from playwright.sync_api._generated import APIResponse
import pytest
from playwright.sync_api import APIRequestContext, expect
import json
from jsonschema import validate
from json_helper import load_json_data

# ... (your fixture code here or in conftest.py) ...

EMPLOYEE_SCHEMA = {
    "type": "object",
    "properties": {
        "employee_id": {"type": "string"},
        "name": {"type": "string"},
        "department": {"type": "string"},
        "salary": {"type": "number"},
        "email": {"type": "string", "format": "email"}, # Optional: enforces email format
        "address": {"type": "string"}
    },
    "required": ["employee_id", "name", "department", "salary", "email", "address"],
    "additionalProperties": False # Ensures no extra unexpected fields are returned
}


def test_home_endpoint(auth_api_context: APIRequestContext):
    print("running the starting endpoint")
    response: APIResponse =  auth_api_context.get("http://127.0.0.1:8000")
    print("Test Response in func : ", response.json())
    expect(response).to_be_ok()


def test_get_all_employees(auth_api_context : APIRequestContext):
    print("Runnnig the All employees GET method")
    response : APIResponse = auth_api_context.get("http://127.0.0.1:8000/employees/get_employees")
    response_api = response.json()
    print("THE EMPLOYEES :", response_api)
    status_code = response_api.get("status_code")
    message = response_api.get("message")
    assert status_code == 200, f"The status code failed it is: {status_code}"
    assert message == "Employees fetched successfully", f"Wrong api message : {message}"

@pytest.mark.skip
def test_create_employee(auth_api_context : APIRequestContext):
    print("Running the test func to Create Employee")
    employee = load_json_data("data.json")
    employee_data = employee["employee_payload"]
    response: APIResponse = auth_api_context.post(url = "http://127.0.0.1:8000/employees/create_employee/" , data = employee_data)
    response_api = response.json()
    status_code = response_api['status_code']
    message = response_api["message"]
    assert  status_code == 201, f"The status code failed it is: {status_code}"
    assert message == "Employee created successfully", f"Wrong Message"
    validate(instance = response_api["data"], schema = EMPLOYEE_SCHEMA)
    print("Schema validation passed successfully!")

def test_get_specific_employee(auth_api_context : APIRequestContext):
    print("Running the test func to Get Specific Employee")
    test_id = load_json_data("data.json")
    emp_id = test_id["search_criteria"]["emp_id"]
    #print("Emp Id : ",emp_id)
    response_api = auth_api_context.get(url = f"http://127.0.0.1:8000/employees/get_employee/{emp_id}")
    response = response_api.json()
    status_code , message , e_id = response["status_code"] , response["message"], response["data"]["employee_id"]
    assert status_code == 200,f"Employee Data not fetched successfully got the status code : {status_code}"
    assert message == "Employee fetched successfully", "ERROR : Not got success message"
    assert e_id == emp_id , "Wrong Emp id fetched"

def test_update_employee_data(auth_api_context : APIRequestContext):
    print("Running the test func to Update Employee Data")
    update_data = load_json_data("data.json")
    emp_id = update_data["update_criteria"]["emp_id"]
    updated_payload = update_data["update_payload"]
    response_api = auth_api_context.put(url = f"http://127.0.0.1:8000/employees/update/{emp_id}", data = updated_payload)
    response = response_api.json()
    print("Response from update employee : ", response)
    status_code , message , e_id = response["status_code"] , response["message"], response["data"]["employee_id"]
    assert status_code == 200,f"Employee Data not updated successfully got the status code : {status_code}"
    assert message == "Employee updated successfully", "ERROR : Not got success message"
    validate(instance = response["data"], schema = EMPLOYEE_SCHEMA)  
    print("Schema validation passed successfully for updated data!")

def test_delete_employee(auth_api_context : APIRequestContext):
    print("Running the test func to Delete Employee Data")
    delete_data = load_json_data("data.json")
    emp_id = delete_data["delete_criteria"]["emp_id"]
    response_api = auth_api_context.delete(url = f"http://127.0.0.1:8000/employees/delete/{emp_id}")
    response = response_api.json()    
    print("Response from delete employee : ", response)
    assert response["status_code"] == 200, f"Employee Data not deleted successfully got the status code : {response['status_code']}"        
    assert response["message"] == "Employee deleted successfully", "ERROR : Not got deletion success message"      
          












   

