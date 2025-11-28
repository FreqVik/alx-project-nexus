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

class PollOptionSchema(BaseModel):
    text: str
    order: Optional[int] = None


class PollOptionResponseSchema(PollOptionSchema):
    id: str

    class Config:
        from_attributes = True


class PollCreateSchema(BaseModel):
    title: str
    description: Optional[str] = None
    author_id: str

    type: PollType = PollType.single
    status: PollStatus = PollStatus.draft

    allow_anonymous: bool = True
    allow_change_vote: bool = False
    max_choices: Optional[int] = None

    options: List[PollOptionSchema] = Field(default_factory=list)


class PollUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[PollType] = None
    status: Optional[PollStatus] = None
    allow_anonymous: Optional[bool] = None
    allow_change_vote: Optional[bool] = None
    max_choices: Optional[int] = None

    options: Optional[List[PollOptionSchema]] = None


class PollResponseSchema(BaseModel):
    id: str
    url: str
    title: str
    description: Optional[str]
    author_id: str
    type: PollType
    status: PollStatus
    allow_anonymous: bool
    allow_change_vote: bool
    max_choices: Optional[int]
    created_at: datetime
    updated_at: datetime

    options: List[PollOptionResponseSchema]

    class Config:
        from_attributes = True
