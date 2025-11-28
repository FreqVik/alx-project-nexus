from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./user_service.db"
    secret_key: str = "VgaA7ZJWu2QzAcG9kpQkBGBCcmSZTgkY"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
