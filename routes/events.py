from typing import List

from fastapi import APIRouter, Depends, status, Query, Path
from db.database import EventSession as Session

from db.database import get_db
from schemas.event_schema import (
    EventCreationSchema,
    AttendeeRegisterSchema,
    EventResponseSchema,
    AttendeeResponseSchema,
)
from services.event_service import EventService

event_router = APIRouter(tags=["Events"])


# Create a new event
@event_router.post("/", response_model=EventResponseSchema, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreationSchema, db: Session = Depends(get_db)):
    return EventService(db).create_event(event)


# List all upcoming events
@event_router.get("/", response_model=List[EventResponseSchema])
def get_events(
    skip: int = Query(0, ge=0, description="How many records to skip from the beginning?"),
    limit: int = Query(10, ge=1, le=100, description="The maximum number of records to return."),
    time_zone: str = Query(default="Asia/Kolkata", description="User time zone"),
    db: Session = Depends(get_db),
):
    return EventService(db).get_all_events(skip=skip, limit=limit, target_timezone=time_zone)


# Register an attendee to a specific event
@event_router.post("/{event_id}/register", response_model=AttendeeResponseSchema)
def register_event(
    attendee: AttendeeRegisterSchema,
    event_id: str = Path(..., description="The ID of the event"),
    db: Session = Depends(get_db),
):
    return EventService(db).register_attendee(event_id=event_id, attendee=attendee)


# Get all attendees of an event
@event_router.get("/{event_id}/attendees", response_model=List[AttendeeResponseSchema])
def get_event_attendees(
    event_id: str = Path(..., description="The ID of the event"),
    skip: int = Query(0, ge=0, description="How many records to skip from the beginning?"),
    limit: int = Query(10, ge=1, le=100, description="The maximum number of records to return."),
    db: Session = Depends(get_db),
):
    return EventService(db).get_attendees(event_id=event_id, skip=skip, limit=limit)
