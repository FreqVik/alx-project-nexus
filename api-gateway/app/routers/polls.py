from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from typing import List, Literal
from fastapi.security import OAuth2PasswordBearer
from ..proxy import reverse_proxy
from config import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

class PollOption(BaseModel):
    text: str
    order: int

class PollCreateBody(BaseModel):
    title: str
    description: str
    author_id: str
    type: Literal["single", "multiple"]
    status: Literal["draft", "published", "closed"]
    allow_anonymous: bool
    allow_change_vote: bool
    max_choices: int
    options: List[PollOption]


@router.post("/")
async def create_poll(request: Request, body: PollCreateBody, token: str = Depends(oauth2_scheme)):
    return await reverse_proxy(settings.poll_service_url, request)


@router.get("/")
async def get_polls(request: Request):
    return await reverse_proxy(settings.poll_service_url, request)


@router.get("/{poll_id}")
async def get_poll(request: Request, poll_id: str):
    return await reverse_proxy(settings.poll_service_url, request)


@router.get("/url/{url}")
async def get_poll_by_url(request: Request, url: str):
    return await reverse_proxy(settings.poll_service_url, request)
