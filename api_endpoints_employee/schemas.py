
from pydantic import BaseModel


class LoginSchema(BaseModel):

    username: str
    password: str


# Common Fields
class EmployeeBase(BaseModel):
    employee_id: str
    name: str
    department: str
    salary: float
    email: str
    address: str

# Create Employee Schema
class EmployeeCreate(EmployeeBase):
    pass

# Response Schema
class EmployeeResponse(EmployeeBase):

    class Config:
        from_attributes = True