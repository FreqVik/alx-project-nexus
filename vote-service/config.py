from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./vote_service.db"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
