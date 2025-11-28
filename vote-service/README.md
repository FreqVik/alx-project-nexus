# Vote Service

This service is responsible for handling votes in a real-time polling application.

## Features

- Cast votes for polls.
- Get real-time vote results via WebSockets.
- Standard API for retrieving vote counts.

## Getting Started

1.  **Install dependencies:**
    ```bash
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```

2.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```

## API Endpoints

-   `POST /votes/`: Cast a new vote.
-   `GET /votes/{poll_id}/results`: Get the current vote counts for a poll.
-   `WS /votes/ws/{poll_id}`: WebSocket endpoint for real-time vote updates.

### WebSocket Usage

Connect to the WebSocket endpoint `/votes/ws/{poll_id}` to receive live updates for a poll. When a new vote is cast for that poll, a JSON message with the updated results will be broadcast to all connected clients.

**Example Message:**
```json
{
  "results": [
    {"option_id": "some-option-id-1", "count": 10},
    {"option_id": "some-option-id-2", "count": 5}
  ]
}
```
