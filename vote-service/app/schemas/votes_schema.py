from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VoteCreateSchema(BaseModel):
    poll_id: str
    option_id: str

class VoteResponseSchema(BaseModel):
    id: str
    poll_id: str
    option_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class VoteCountSchema(BaseModel):
    option_id: str
    count: int
