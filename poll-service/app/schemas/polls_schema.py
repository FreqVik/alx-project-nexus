from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional
from uuid import UUID
from datetime import datetime

# Enums (same as your models)
class PollType(str, Enum):
    single = "single"
    multiple = "multiple"
    ranked = "ranked"

class PollStatus(str, Enum):
    draft = "draft"
    scheduled = "scheduled"
    active = "active"
    closed = "closed"

# Option schema
class PollOptionSchema(BaseModel):
    text: str
    order: Optional[int] = None

# Poll create schema
class PollCreateSchema(BaseModel):
    title: str
    description: Optional[str] = None
    author_id: str
    type: PollType = PollType.single
    status: PollStatus = PollStatus.draft
    allow_anonymous: Optional[bool] = True
    allow_change_vote: Optional[bool] = False
    max_choices: Optional[int] = None
    options: Optional[List[PollOptionSchema]] = []

# Poll update schema
class PollUpdateSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    type: Optional[PollType]
    status: Optional[PollStatus]
    allow_anonymous: Optional[bool]
    allow_change_vote: Optional[bool]
    max_choices: Optional[int]
    options: Optional[List[PollOptionSchema]]

# Poll response schema
class PollResponseSchema(BaseModel):
    id: str
    title: str
    description: Optional[str]
    author_id: str
    type: PollType
    status: PollStatus
    allow_anonymous: bool
    allow_change_vote: bool
    max_choices: Optional[int]
    options: List[PollOptionSchema] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
