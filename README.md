# UVote

UVote is an interactive online polling application built with a microservices architecture. It provides separate services for users (auth), polls (management), votes (real‑time voting), and an API Gateway that exposes a single entry point for clients. Both backend and frontend developers can run and test the system locally using FastAPI’s interactive docs and simple `curl` commands.

## Architecture
- **User Service (5000):** Registration and login, issues JWT access tokens.
- **Poll Service (7000):** Create/list/fetch polls. Poll creation requires a Bearer token.
- **Vote Service (8000):** Cast votes, enforce one vote per IP per poll, stream updates via WebSocket.
- **API Gateway (9000):** Reverse proxy to all services for HTTP and WebSocket, provides a unified Swagger UI for testing.

## Prerequisites
- Linux/macOS/Windows with Bash shell.
- Python `3.12` installed.
- Uvicorn available via the project virtual environments under each service.
- Ports available: `5000`, `7000`, `8000`, `9000`.

## Quick Start
You can run each service separately, then use the API Gateway at `http://127.0.0.1:9000`.

### 1) Start User Service (Auth)
```
cd user-service
python3 -m venv env && source env/bin/activate  # optional if not already created
pip install -r requirements.txt
uvicorn main:app --port 5000
```

### 2) Start Poll Service
```
cd poll-service
python3 -m venv env && source env/bin/activate  # optional if not already created
pip install -r requirements.txt
uvicorn main:app --port 7000
```

### 3) Start Vote Service
```
cd vote-service
python3 -m venv env && source env/bin/activate  # optional if not already created
pip install -r requirements.txt
uvicorn main:app --port 8000
```

### 4) Start API Gateway
```
cd api-gateway
python3 -m venv env && source env/bin/activate  # optional if not already created
pip install -r requirements.txt
uvicorn main:app --port 9000
```

Once all services are running, open `http://127.0.0.1:9000/docs` for an end‑to‑end test experience.

## Testing via API Gateway
All paths below are relative to `http://127.0.0.1:9000`.

### 1) Register
- Swagger: `POST /users/register`
- `curl`:
```
curl -X POST http://127.0.0.1:9000/users/register \
	-H 'Content-Type: application/json' \
	-d '{"username":"alice","password":"secret"}'
```

### 2) Login and get JWT
- Swagger: `POST /users/token` (uses form fields in the docs)
- `curl` (form data):
```
curl -X POST http://127.0.0.1:9000/users/token \
	-H 'Content-Type: application/x-www-form-urlencoded' \
	-d 'username=alice&password=secret'
```
Copy the `access_token` from the response.

### 3) Authorize in Swagger
- In `http://127.0.0.1:9000/docs`, click `Authorize` and enter: `Bearer <access_token>`.

### 4) Create a Poll
- Swagger: `POST /polls/` shows the required JSON body and requires the Bearer token.
- Example body shape:
```
{
	"question": "Your favorite language?",
	"options": [
		{"text": "Python"},
		{"text": "JavaScript"},
		{"text": "Go"}
	]
}
```
- `curl`:
```
curl -X POST http://127.0.0.1:9000/polls/ \
	-H 'Authorization: Bearer <access_token>' \
	-H 'Content-Type: application/json' \
	-d '{"question":"Your favorite language?","options":[{"text":"Python"},{"text":"JavaScript"},{"text":"Go"}]}'
```
Response includes `id` and a unique `url` for the poll.

### 5) List Polls
- Swagger: `GET /polls/`
- `curl`:
```
curl http://127.0.0.1:9000/polls/
```

### 6) Get Poll by ID or URL
- Swagger: `GET /polls/{poll_id}` and `GET /polls/url/{url}`
- `curl`:
```
curl http://127.0.0.1:9000/polls/<poll_id>
curl http://127.0.0.1:9000/polls/url/<url>
```

### 7) Cast a Vote
- Swagger: `POST /votes/` shows the required JSON body.
- Example body shape:
```
{
	"poll_id": "<poll_id>",
	"option_id": "<option_id>"
}
```
- `curl`:
```
curl -X POST http://127.0.0.1:9000/votes/ \
	-H 'Content-Type: application/json' \
	-d '{"poll_id":"<poll_id>","option_id":"<option_id>"}'
```
Note: One vote per IP per poll is enforced.

### 8) Get Vote Results
- Swagger: `GET /votes/{poll_id}`
- `curl`:
```
curl http://127.0.0.1:9000/votes/<poll_id>
```
Returns counts per option.

### 9) WebSocket Updates (Live)
- Path: `ws://127.0.0.1:9000/votes/ws/<poll_id>`
- Connect a WebSocket client to receive live vote updates.

## Service‑level Testing (Optional)
You can also hit each service directly (bypassing the gateway) on `http://127.0.0.1:{PORT}/docs` for debugging.

## Troubleshooting
- **Vote Service not starting (Exit Code 1):** Ensure dependencies are installed in `vote-service/env` and running `uvicorn main:app --port 8000` from `vote-service` directory.
- **401 when creating polls:** You must login via `/users/token` and use `Authorize` in Swagger or include `Authorization: Bearer <token>` in requests.
- **Form vs JSON bodies in the Gateway:** Login uses `application/x-www-form-urlencoded`; other endpoints use JSON. The gateway handles both correctly.
- **Swagger “Duplicate Operation ID” warnings:** The gateway uses explicit, per‑method routes to avoid this.

## Notes for Frontend Devs
- Prefer the API Gateway at `http://127.0.0.1:9000` to avoid cross‑service URLs.
- WebSocket for live results: `ws://127.0.0.1:9000/votes/ws/<poll_id>`.
- Poll creation requires an auth token; plan flows: register → login → authorize → create poll → vote → subscribe for updates.

