# API Gateway

This service acts as a single entry point for the entire polling application, routing requests to the appropriate backend microservice.

## Features

-   **Reverse Proxy:** Forwards HTTP requests to the `user-service`, `poll-service`, and `vote-service`.
-   **WebSocket Proxy:** Forwards WebSocket connections to the `vote-service` for real-time updates.
-   **Centralized Entry Point:** Simplifies client-side configuration and provides a single address for the entire application.

## Getting Started

1.  **Install dependencies:**

    ```bash
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```

2.  **Configure Service URLs:**
    Ensure the `.env` file contains the correct URLs for the backend services. By default, it's configured for:
    -   `user-service` on port `5000`
    -   `poll-service` on port `7000`
    -   `vote-service` on port `8000`

3.  **Run the application:**

    ```bash
    uvicorn main:app --reload --port 9000
    ```

    The API Gateway will run on port `9000` by default.

## Routing

-   Requests to `/users/...` are routed to the **User Service**.
-   Requests to `/polls/...` are routed to the **Poll Service**.
-   Requests to `/votes/...` are routed to the **Vote Service**.
-   WebSocket connections to `/votes/ws/{poll_id}` are proxied to the **Vote Service**.
