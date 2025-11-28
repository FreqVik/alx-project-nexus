from fastapi import APIRouter, Request, WebSocket, Body
from pydantic import BaseModel
from typing import List
from ..proxy import reverse_proxy, websocket_proxy_endpoint
from config import settings

router = APIRouter()

class VoteCreateBody(BaseModel):
    poll_id: str
    option_id: str

class VoteCount(BaseModel):
    option_id: int
    count: int

@router.websocket("/ws/{poll_id}")
async def vote_websocket_proxy(websocket: WebSocket, poll_id: str):
    """
    WebSocket proxy for the Vote Service.
    """
    ws_url = f"{settings.vote_service_url.replace('http', 'ws')}/votes/ws/{poll_id}"
    await websocket_proxy_endpoint(websocket, ws_url)


@router.post("/")
async def cast_vote(request: Request, body: VoteCreateBody):
    return await reverse_proxy(settings.vote_service_url, request)


@router.get("/{poll_id}", response_model=List[VoteCount])
async def get_votes(request: Request, poll_id: str):
    return await reverse_proxy(settings.vote_service_url, request)
