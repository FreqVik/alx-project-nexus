from sqlalchemy.orm import Session
from models.poll import Poll, PollOption
from schemas.poll import (
    PollCreateSchema,
    PollUpdateSchema
)
import uuid


class PollService:
    def __init__(self, db:Session):
        self.db = db

    def create_poll(self, data: PollCreateSchema):
       """
       Create a new poll with the given data.
       """
       poll = Poll(
           id=str(uuid.uuid4()),
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
       
       if data.options:
        for index, option_schema in enumerate(data.options):
            option = PollOption(
                id=str(uuid.uuid4()),
                poll_id=poll.id,
                text=option_schema.text,
                order=index
            )
            self.db.add(option)
        self.db.commit()
        self.db.refresh(poll)

        return poll

    def get_poll(self, poll_id: str):
        """
        Retrieve a poll by its ID.
        """
        poll = self.db.query(Poll).filter(Poll.id == poll_id).first()
        return poll
    
    def list_polls(self):
        """
        Retrieve a list of all polls.
        """
        polls = self.db.query(Poll).all()
        return polls
    
    def update_poll(self, poll_id: str, data: PollUpdateSchema):
        """
        Update an existing poll with the given data.
        """
        poll = self.db.query(Poll).filter(Poll.id == poll_id).first()
        if not poll:
            return None

        for key, value in data.dict(exclude_unset=True).items():
            setattr(poll, key, value)

        self.db.commit()
        self.db.refresh(poll)
        return poll
    
    def delete_poll(self, poll_id: str):
        """
        Delete a poll by its ID.
        """
        poll = self.db.query(Poll).filter(Poll.id == poll_id).first()
        if not poll:
            return None

        self.db.delete(poll)
        self.db.commit()
        return poll