from sqlalchemy import SQLAlchemy
from database.db import Base
import uuid
from sqlalchemy import Column, String, Text, DateTime, Boolean, Enum, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum



class PollType(str, enum.Enum):
    single = "single"
    multiple = "multiple"
    ranked = "ranked"

class PollStatus(str, enum.Enum):
    draft = "draft"
    scheduled = "scheduled"
    active = "active"
    closed = "closed"


class Polls(Base):
    __tablename__ = "polls"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4))
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    author_id = Column(String(36))
    type = Column(Enum(PollType), default=PollType.single)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    status = Column(Enum(PollStatus), default=None)
    allow_anonymous = Column(Boolean, default=True)
    allow_change_vote = Column(Boolean, default=False)
    max_choices = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    options = relationship("PollOption", back_populates="poll", cascade="all, delete-orphan")


class PollOption(Base):
    __tablename__ = "poll_options"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    poll_id = Column(String(36), ForeignKey("polls.id", ondelete="CASCADE"), nullable=False)
    text = Column(String(255), nullable=False)
    order = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    poll = relationship("Poll", back_populates="options")

