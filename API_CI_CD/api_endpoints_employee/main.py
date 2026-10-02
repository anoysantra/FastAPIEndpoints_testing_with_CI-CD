from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

import crud
import schemas
import models

from database import SessionLocal

from auth import (
    #verify_password,
    create_access_token,
    verify_token,
    admin_required
)


app = FastAPI()


# JWT Token Scheme
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


# Database Dependency
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# LOGIN API
@app.post("/login")
def login(
    user: schemas.LoginSchema,
    db: Session = Depends(get_db)
):

    try:

        db_user = db.query(models.User).filter(
            models.User.username == user.username
        ).first()

        if not db_user:

            raise HTTPException(
                status_code=401,
                detail="Invalid username"
            )

        # Plain text password comparison
        if user.password != db_user.password:

            raise HTTPException(
                status_code=401,
                detail="Invalid password"
            )

        access_token = create_access_token(
            data={
                "sub": db_user.username,
                "role": db_user.user_type
            }
        )

        return {
            "success": True,
            "status_code": 200,
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Login failed: {str(e)}"
        )

# HOME Endpoint
@app.get("/")
def home():

    return {
        "success": True,
        "status_code": 200,
        "message": "Employee CRUD API is running"
    }


# CREATE Employee
@app.post(
    "/employees/create_employee/",
    status_code=status.HTTP_201_CREATED
)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):

    verify_token(token)

    try:

        created_employee = crud.create_employee(
            db,
            employee
        )

        return {
            "success": True,
            "status_code": 201,
            "message": "Employee created successfully",
            "data": created_employee
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to create employee: {str(e)}"
        )


# GET All Employees
@app.get("/employees/get_employees/")
def get_all_employees(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):

    verify_token(token)

    try:

        employees = crud.get_all_employees(db)

        if not employees:

            return {
                "success": False,
                "status_code": 404,
                "message": "No employees found",
                "data": []
            }

        return {
            "success": True,
            "status_code": 200,
            "message": "Employees fetched successfully",
            "data": employees
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch employees: {str(e)}"
        )


# GET Employee By ID
@app.get("/employees/get_employee/{employee_id}")
def get_employee_by_id(
    employee_id: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):

    verify_token(token)

    try:

        employee = crud.get_employee_by_id(
            db,
            employee_id
        )

        if not employee:

            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        return {
            "success": True,
            "status_code": 200,
            "message": "Employee fetched successfully",
            "data": employee
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch employee: {str(e)}"
        )


# UPDATE Employee
@app.put("/employees/update/{employee_id}")
def update_employee(
    employee_id: str,
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):

    #verify_token(token)
    admin_required(token)


    try:

        updated_employee = crud.update_employee(
            db,
            employee_id,
            employee
        )

        if not updated_employee:

            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        return {
            "success": True,
            "status_code": 200,
            "message": "Employee updated successfully",
            "data": updated_employee
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to update employee: {str(e)}"
        )


# DELETE Employee
@app.delete("/employees/delete/{employee_id}")
def delete_employee(
    employee_id: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):

    #verify_token(token)
    admin_required(token)

    try:

        deleted_employee = crud.delete_employee(
            db,
            employee_id
        )

        if not deleted_employee:

            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        return {
            "success": True,
            "status_code": 200,
            "message": "Employee deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete employee: {str(e)}"
        )