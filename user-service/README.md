# User Service

This service handles user authentication (registration and login) for the polling application.

## Features

-   User registration with secure password hashing.
-   User login with JWT token generation.

## Getting Started

1.  **Install dependencies:**

    ```bash
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```

2.  **Run the application:**

    ```bash
    uvicorn main:app --reload --port 8001
    ```

    The service will run on port 8001 by default.

## API Endpoints

-   `POST /register`: Create a new user.
-   `POST /login`: Log in and receive a JWT access token.

### How to Authenticate

1.  **Register a user:**
    Send a `POST` request to `/register` with a username, email, and password.

2.  **Log in:**
    Send a `POST` request to `/login` with the `username` and `password` as form data. The response will contain an `access_token`.

3.  **Access protected endpoints:**
    Include the `access_token` in the `Authorization` header of your requests as a Bearer token.
    Example: `Authorization: Bearer <your_token>`
