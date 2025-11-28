from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.schemas.polls_schema import (
    PollCreateSchema,
    PollUpdateSchema,
    PollResponseSchema
)
from app.services.poll_service import PollService
from app.database.db import get_db
from app.utils.url import get_poll_url

router = APIRouter(
    prefix="/polls",
    tags=["Polls"]
)


@router.post("/", response_model=PollResponseSchema)
def create_poll(payload: PollCreateSchema, request: Request, db: Session = Depends(get_db)):
    service = PollService(db)
    poll = service.create_poll(payload)
    poll.url = get_poll_url(request, poll.url)
    return poll


@router.get("/url/{poll_url}", response_model=PollResponseSchema)
def get_poll_by_url(poll_url: str, request: Request, db: Session = Depends(get_db)):
    service = PollService(db)
    poll = service.get_poll_by_url(poll_url)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    poll.url = get_poll_url(request, poll.url)
    return poll


@router.get("/{poll_id}", response_model=PollResponseSchema)
def get_poll(poll_id: str, request: Request, db: Session = Depends(get_db)):
    service = PollService(db)
    poll = service.get_poll(poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    poll.url = get_poll_url(request, poll.url)
    return poll


@router.get("/", response_model=list[PollResponseSchema])
def list_polls(
    request: Request, db: Session = Depends(get_db)
):
    service = PollService(db)
    polls = service.list_polls()
    for poll in polls:
        poll.url = get_poll_url(request, poll.url)
    return polls


@router.patch("/{poll_id}", response_model=PollResponseSchema)
def update_poll(poll_id: str, payload: PollUpdateSchema, request: Request, db: Session = Depends(get_db)):
    service = PollService(db)
    poll = service.update_poll(poll_id, payload)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    poll.url = get_poll_url(request, poll.url)
    return poll


@router.delete("/{poll_id}", response_model=PollResponseSchema)
def delete_poll(poll_id: str, db: Session = Depends(get_db)):
    service = PollService(db)
    poll = service.delete_poll(poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    return poll