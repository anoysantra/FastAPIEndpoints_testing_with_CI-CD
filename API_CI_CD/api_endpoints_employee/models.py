from sqlalchemy import Column, Integer, String, Float

from database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True)

    password = Column(String(255))

    user_type = Column(String(50))

class Employee(Base):

    __tablename__ = "employees_fastapi"

    employee_id = Column(String(10), primary_key=True, index=True)
    name = Column(String(100))
    department = Column(String(100))
    salary = Column(Float)
    email = Column(String(100), unique=True)
    address = Column(String(255))