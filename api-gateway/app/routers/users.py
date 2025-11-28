from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from ..proxy import reverse_proxy
from config import settings

router = APIRouter()

class UserCreateBody(BaseModel):
    username: str
    email: str
    password: str


@router.post("/register")
async def register_user(request: Request, body: UserCreateBody):
    return await reverse_proxy(settings.user_service_url, request, strip_prefix="/users")


@router.post("/token")
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    return await reverse_proxy(settings.user_service_url, request, strip_prefix="/users")
