from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    user_service_url: str 
    poll_service_url: str
    vote_service_url: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
