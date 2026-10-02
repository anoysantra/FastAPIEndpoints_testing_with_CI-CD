# 🚀 FastAPI Employee Management System

This project is a backend API system built using FastAPI, MySQL, and JWT Authentication with Role-Based Access Control (RBAC).

It simulates a real-world employee management system where:
- Admins can create, update, delete, and view employees
- Employees can only view data
- Secure login is required for all protected actions

---

# 💡 What This Project Does

- User logs in with username & password
- System validates credentials
- JWT token is generated
- Token is used for all API requests
- Role (admin/employee) decides access level

---

# 🛠️ Database Setup (MySQL)

CREATE DATABASE employee_db;

USE employee_db;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    user_type VARCHAR(20)
);

CREATE TABLE employees_fastapi (
    employee_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(100),
    salary FLOAT,
    email VARCHAR(100),
    address VARCHAR(200)
);

---

# 🔗 Database Connection

DATABASE_URL = "mysql+pymysql://root:username@localhost:3306/employee_db"

---

# ▶️ Run Project

uvicorn main:app --reload

API Base URL:
http://127.0.0.1:8000

Swagger UI:
http://127.0.0.1:8000/docs

---

# 🔐 Authentication Flow

## Login API

POST /login

Request:
{
  "username": "admin",
  "password": "admin1"
}

Response:
{
  "success": true,
  "status_code": 200,
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}

---

# 🔑 JWT Token Usage

Use this token in all protected APIs:

Authorization: Bearer <access_token>

---

# 👥 User Roles

Role        Permissions
admin       Full CRUD access
employee    Read-only access

---

# 🧑‍💼 Employee APIs

---

## ➕ Create Employee (ADMIN ONLY)

POST /employees

Request:
{
  "employee_id": "E101",
  "name": "Rahul Sharma",
  "department": "IT",
  "salary": 75000,
  "email": "rahul@example.com",
  "address": "Bangalore"
}

Response:
{
  "success": true,
  "message": "Employee created successfully"
}

---

## 📄 Get All Employees

GET /employees

Response:
[
  {
    "employee_id": "E101",
    "name": "Rahul Sharma",
    "department": "IT",
    "salary": 75000,
    "email": "rahul@example.com",
    "address": "Bangalore"
  }
]

---

## 🔍 Get Employee by ID

GET /employees/E101

---

## ✏️ Update Employee (ADMIN ONLY)

PUT /employees/E101

Request:
{
  "name": "Rahul Updated",
  "department": "Engineering",
  "salary": 90000,
  "email": "rahul_new@example.com",
  "address": "Hyderabad"
}

---

## ❌ Delete Employee (ADMIN ONLY)

DELETE /employees/E101

---

# 🔐 Role-Based Access Logic

if current_user["role"] != "admin":
    raise HTTPException(status_code=403, detail="Admin access required")

---

# 🧠 JWT Payload Example

{
  "sub": "admin1",
  "role": "admin",
  "exp": 1779536525
}

---

# 🧪 Testing Flow (Postman)

1. Call /login
2. Copy access token
3. Add to headers:

Authorization: Bearer <token>

4. Call employee APIs

---

# ⚠️ Important Notes

- Passwords are stored in plain text (for learning only)
- Use bcrypt hashing in production
- Keep JWT secret secure
- Never expose tokens publicly

---

# 🎯 Summary

This project demonstrates:
- JWT Authentication
- Role-Based Access Control
- FastAPI CRUD APIs
- MySQL Integration
- Production-style backend design

---

# 💡 Real-World Use

This system works like a mini HR backend where companies:
- Secure login employees
- Restrict access based on roles
- Manage employee records efficiently
