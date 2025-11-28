from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
    Request,
    HTTPException,
)
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Dict

from app.schemas.votes_schema import VoteCreateSchema, VoteResponseSchema, VoteCountSchema
from app.services.vote_service import VoteService
from app.database.db import get_db

router = APIRouter(prefix="/votes", tags=["Votes"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, poll_id: str):
        await websocket.accept()
        if poll_id not in self.active_connections:
            self.active_connections[poll_id] = []
        self.active_connections[poll_id].append(websocket)

    def disconnect(self, websocket: WebSocket, poll_id: str):
        if poll_id in self.active_connections:
            self.active_connections[poll_id].remove(websocket)

    async def broadcast(self, poll_id: str, message: dict):
        if poll_id in self.active_connections:
            for connection in self.active_connections[poll_id]:
                await connection.send_json(message)

manager = ConnectionManager()

@router.post("/", response_model=VoteResponseSchema)
async def cast_vote(
    payload: VoteCreateSchema,
    request: Request,
    db: Session = Depends(get_db),
):
    service = VoteService(db)
    ip_address = request.client.host
    try:
        vote = service.create_vote(payload, ip_address)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="You have already voted on this poll.")
    
    # Broadcast updated results
    results = service.get_vote_results(payload.poll_id)
    await manager.broadcast(payload.poll_id, {"results": [r.dict() for r in results]})
    
    return vote

@router.get("/{poll_id}/results", response_model=List[VoteCountSchema])
def get_results(poll_id: str, db: Session = Depends(get_db)):
    service = VoteService(db)
    return service.get_vote_results(poll_id)

@router.websocket("/ws/{poll_id}")
async def websocket_endpoint(websocket: WebSocket, poll_id: str, db: Session = Depends(get_db)):
    await manager.connect(websocket, poll_id)
    try:
        # Send initial results on connect
        service = VoteService(db)
        results = service.get_vote_results(poll_id)
        await websocket.send_json({"results": [r.dict() for r in results]})

        while True:
            # Keep the connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, poll_id)
