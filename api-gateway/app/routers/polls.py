from fastapi import APIRouter, Request
from ..proxy import reverse_proxy
from config import settings

router = APIRouter()


@router.post("/")
async def create_poll(request: Request):
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
