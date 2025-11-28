from sqlalchemy.orm import Session
from app.models.polls import Polls, PollOption, PollStatus
from app.schemas.polls_schema import (
    PollCreateSchema,
    PollUpdateSchema
)
from app.utils.url import generate_unique_url
from config import settings
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PollService:
    def __init__(self, db: Session):
        self.db = db

    def create_poll(self, data: PollCreateSchema):
        unique_url = generate_unique_url(self.db, Polls)
        poll = Polls(
            url=unique_url,
            title=data.title,
            description=data.description,
            author_id=data.author_id,
            type=data.type,
            status=data.status,
            allow_anonymous=data.allow_anonymous,
            allow_change_vote=data.allow_change_vote,
            max_choices=data.max_choices
        )

        self.db.add(poll)
        self.db.flush()

        for index, opt in enumerate(data.options):
            option = PollOption(
                poll_id=poll.id,
                text=opt.text,
                order=index
            )
            self.db.add(option)

        self.db.commit()
        self.db.refresh(poll)
        
        return poll

    def get_poll(self, poll_id: str):
        return self.db.query(Polls).filter(Polls.id == poll_id).first()
    
    def get_poll_by_url(self, poll_url: str):
        return self.db.query(Polls).filter(Polls.url == poll_url).first()

    def list_polls(self):
        return self.db.query(Polls).all()

    def update_poll(self, poll_id: str, data: PollUpdateSchema):
        poll = self.get_poll(poll_id)
        if not poll:
            return None

        old_status = poll.status
        updated_fields = []
        
        for key, value in data.dict(exclude_unset=True, exclude={"options"}).items():
            if getattr(poll, key) != value:
                updated_fields.append(key)
            setattr(poll, key, value)

        # Update options if provided
        if data.options is not None:
            updated_fields.append("options")
            # Remove old options
            self.db.query(PollOption).filter(PollOption.poll_id == poll_id).delete()

            # Add new ones
            for index, opt in enumerate(data.options):
                option = PollOption(
                    poll_id=poll.id,
                    text=opt.text,
                    order=index
                )
                self.db.add(option)

        poll.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(poll)
        
        return poll

    def delete_poll(self, poll_id: str):
        poll = self.get_poll(poll_id)
        if not poll:
            return None

        self.db.delete(poll)
        self.db.commit()
        return poll
