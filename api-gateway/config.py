from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    user_service_url: str = "http://127.0.0.1:5000"
    poll_service_url: str = "http://127.0.0.1:7000"
    vote_service_url: str = "http://127.0.0.1:8000"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
