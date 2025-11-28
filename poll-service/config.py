from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./poll_service.db"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
