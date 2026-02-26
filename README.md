# 💰 Personal Expense Tracker API

A RESTful API project for personal finance management, Built following the [roadmap.sh Expense Tracker API](https://roadmap.sh/projects/expense-tracker-api).

## 🎯 Overview

This project serves as the core backend for an expense tracking application. It allows users to securely register, authenticate via JWT, and manage their personal expenses. The system ensures strict data isolation—users can only access and modify their own financial records, functioning as a solid foundation for a personal digital wallet system.

## 🛠 Tech Stack

* **Framework:** FastAPI (Python 3)
* **Database:** SQLite + SQLModel (ORM)
* **Authentication:** OAuth2 with JWT (JSON Web Tokens)
* **Security:** PassLib (argon2 password hashing)

## ✨ Key Features

* **Secure Authentication Flow:** User registration and login using OAuth2PasswordBearer. Passwords are encrypted before storing in the database.
* **Data Isolation (IDOR Prevention):** Every expense is hard-tied to a `user_id` via Foreign Keys. API endpoints strictly validate tokens to ensure users only interact with their own data.
* **CRUD Operations:** Full lifecycle management of expenses (Create, Read, Update, Delete).
* **Strict Data Validation:** Utilizing Pydantic schemas and Python Enums to enforce data integrity (e.g., categorizing expenses strictly into predefined types like Groceries, Leisure, Health, etc.).
* **Pagination & Filtering:** Efficient data retrieval using limit and offset for large transaction histories.

## 📂 Project Structure

The codebase is organized modularly to scale easily:

    expense-tracker-api/
    ├── app/
    │   ├── api/              # API Routers & Endpoints
    │   ├── core/             # Security (JWT configuration)
    │   ├── db/               # Database engine & setup
    │   ├── models_and_schemas/ # SQLModel tables & Pydantic validation schemas
    │   ├── repositories/     # Database interaction logic (UserRepo, ExpenseRepo)
    │   ├── utils/            # Helper functions (Password hashing)
    │   └── main.py           # FastAPI application instance
    ├── .env                  # Environment variables (Ignored in Git)
    └── .gitignore            # Git exclusion rules

## 🚀 Local Setup & Installation

Follow these steps to run the API on your local machine:

**1. Clone the repository**
    git clone https://github.com/dablank192/expense-tracker-api.git
    cd expense-tracker-api

**2. Create a virtual environment**
    python -m venv .venv
    # On Windows:
    .venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate

**3. Install dependencies**
    pip install -r requirements.txt

**4. Environment Variables**
Create a .env file in the root directory and add your secret keys:
    SECRET_KEY="your-super-secret-jwt-key"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30

**5. Run the Server**
    uvicorn app.main:app --reload

*Note: The system is configured to auto-generate the database.db SQLite file upon the first run. You do not need to run manual migration scripts.*
