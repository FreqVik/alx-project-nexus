from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.schemas.users_schema import UserCreateSchema, UserResponseSchema, TokenSchema
from app.services.user_service import UserService
from app.database.db import get_db
from app.security import create_access_token
from config import settings

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=UserResponseSchema)
def register_user(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    service = UserService(db)
    db_user = service.get_user_by_username(user_data.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return service.create_user(user_data=user_data)


@router.post("/token", response_model=TokenSchema)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    service = UserService(db)
    user = service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
