from fastapi import FastAPI
from app.routers.votes import router as votes_router
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import create_tables
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Vote Service", version="1.0.0")

@app.on_event("startup")
def on_startup():
    create_tables()

app.include_router(votes_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Vote Service API"}
