from sqlalchemy.orm import Session

import models
import schemas


# CREATE Employee
def create_employee(
    db: Session,
    employee: schemas.EmployeeCreate
):

    new_employee = models.Employee(
        employee_id = employee.employee_id,
        name=employee.name,
        department=employee.department,
        salary=employee.salary,
        email=employee.email,
        address=employee.address
    )

    db.add(new_employee)

    db.commit()

    db.refresh(new_employee)

    return new_employee


# GET All Employees
def get_all_employees(db: Session):

    return db.query(models.Employee).all()


# GET Employee By ID
def get_employee_by_id(
    db: Session,
    employee_id: str
):

    return db.query(models.Employee).filter(
        models.Employee.employee_id == employee_id
    ).first()


# UPDATE Employee
def update_employee(
    db: Session,
    employee_id: str,
    employee: schemas.EmployeeCreate
):

    existing_employee = db.query(models.Employee).filter(
        models.Employee.employee_id == employee_id
    ).first()

    if not existing_employee:

        return None

    existing_employee.name = employee.name
    existing_employee.department = employee.department
    existing_employee.salary = employee.salary
    existing_employee.email = employee.email
    existing_employee.address = employee.address

    db.commit()

    db.refresh(existing_employee)

    return existing_employee


# DELETE Employee
def delete_employee(
    db: Session,
    employee_id: str
):

    employee = db.query(models.Employee).filter(
        models.Employee.employee_id == employee_id
    ).first()

    if not employee:

        return None

    db.delete(employee)

    db.commit()

    return employee