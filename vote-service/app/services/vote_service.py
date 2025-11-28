from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from app.models.votes import Vote
from app.schemas.votes_schema import VoteCreateSchema, VoteCountSchema
from typing import List

class VoteService:
    def __init__(self, db: Session):
        self.db = db

    def create_vote(self, vote_data: VoteCreateSchema, ip_address: str) -> Vote:
        
        existing_vote = self.db.query(Vote).filter_by(poll_id=vote_data.poll_id, ip_address=ip_address).first()
        if existing_vote:
            raise IntegrityError("IP address has already voted on this poll.", params=None, orig=None)

        vote = Vote(
            poll_id=vote_data.poll_id,
            option_id=vote_data.option_id,
            ip_address=ip_address
        )
        self.db.add(vote)
        self.db.commit()
        self.db.refresh(vote)
        return vote

    def get_vote_results(self, poll_id: str) -> List[VoteCountSchema]:
        results = (
            self.db.query(Vote.option_id, func.count(Vote.id).label("count"))
            .filter(Vote.poll_id == poll_id)
            .group_by(Vote.option_id)
            .all()
        )
        return [VoteCountSchema(option_id=option_id, count=count) for option_id, count in results]
