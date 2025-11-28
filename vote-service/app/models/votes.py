import uuid
from sqlalchemy import Column, String, DateTime, Index
from datetime import datetime
from app.database.db import Base

class Vote(Base):
    __tablename__ = "votes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    poll_id = Column(String(36), nullable=False, index=True)
    option_id = Column(String(36), nullable=False)
    ip_address = Column(String(45), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (Index("ix_poll_id_ip_address", "poll_id", "ip_address", unique=True),)
