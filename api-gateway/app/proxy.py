import httpx
from fastapi import Request, Response, WebSocket
from starlette.websockets import WebSocketDisconnect
import websockets
import asyncio

client = httpx.AsyncClient()

async def reverse_proxy(url: str, request: Request, strip_prefix: str | None = None):
    """
    Generic reverse proxy function.
    """
    # Extract the path from the request and optionally strip a router prefix
    service_path = request.scope.get("path") or "/"
    if strip_prefix and service_path.startswith(strip_prefix):
        service_path = service_path[len(strip_prefix):] or "/"
    downstream_url = f"{url}{service_path}"
    
    headers = dict(request.headers)
    headers.pop("host", None)
    # Prevent mismatched body/length issues when re-encoding form/json
    headers.pop("content-length", None)

    try:
        # Body may be already consumed by upstream FastAPI dependencies.
        # Use cached body if present; otherwise try to read once.
        # Determine how to forward the request body
        data = None
        content = None
        content_type = headers.get("content-type", "")
        req_path = service_path

        if request.method in ("POST", "PUT", "PATCH") and ("application/x-www-form-urlencoded" in content_type or req_path.endswith("/users/token")):
            # Parse form and forward as form data (prevents stream-consumed errors)
            try:
                form = await request.form()
                data = dict(form)
            except RuntimeError:
                data = None
        else:
            # Forward raw body (JSON, etc.) when available
            try:
                content = await request.body()
            except RuntimeError:
                content = None

        r = await client.request(
            method=request.method,
            url=downstream_url,
            headers=headers,
            params=request.query_params,
            data=data,
            content=content,
            timeout=60.0,
        )
        # Copy headers from the response, excluding certain problematic ones
        response_headers = dict(r.headers)
        response_headers.pop("content-encoding", None)
        response_headers.pop("transfer-encoding", None)

        return Response(
            content=r.content,
            status_code=r.status_code,
            headers=response_headers,
        )
    except httpx.RequestError as e:
        return Response(
            content=f"An error occurred while proxying the request: {e}",
            status_code=502,
        )

async def websocket_proxy_endpoint(websocket: WebSocket, upstream_url: str):
    """
    Generic WebSocket proxy function.
    """
    await websocket.accept()
    try:
        async with websockets.connect(upstream_url) as upstream_ws:
            # Coroutine to forward messages from client to upstream
            async def forward_to_upstream():
                while True:
                    data = await websocket.receive_text()
                    await upstream_ws.send(data)

            # Coroutine to forward messages from upstream to client
            async def forward_to_client():
                while True:
                    data = await upstream_ws.recv()
                    await websocket.send_text(data)

            # Run both coroutines concurrently
            task1 = asyncio.create_task(forward_to_upstream())
            task2 = asyncio.create_task(forward_to_client())
            
            # Wait for either task to complete (which means a disconnect)
            done, pending = await asyncio.wait(
                [task1, task2], return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancel pending tasks to clean up
            for task in pending:
                task.cancel()

    except (WebSocketDisconnect, websockets.exceptions.ConnectionClosed) as e:
        print(f"WebSocket connection closed: {e}")
    except Exception as e:
        print(f"An error occurred with WebSocket proxy: {e}")
    finally:
        # Ensure the client connection is closed if it's not already
        if websocket.client_state != "DISCONNECTED":
            await websocket.close()
            print("Client WebSocket connection closed.")
