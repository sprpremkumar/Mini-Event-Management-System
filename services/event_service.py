from datetime import timezone

from fastapi import HTTPException

from db.database import EventSession
from models.event import Event, Attendee
from schemas.event_schema import EventCreationSchema, AttendeeRegisterSchema
from utils import convert_to_timezone


class EventService:
    def __init__(self, db: EventSession):
        """
        Initializes the EventService with a SQLAlchemy database session.
        """
        self.db = db

    def create_event(self, event: EventCreationSchema) -> Event:
        """
        Creates a new event and stores it in the database.
        """
        start_time_utc = event.start_time.astimezone(timezone.utc).replace(tzinfo=None)
        end_time_utc = event.end_time.astimezone(timezone.utc).replace(tzinfo=None)
        new_event = Event(
            name=event.name,
            location=event.location,
            start_time=start_time_utc,
            end_time=end_time_utc,
            max_capacity=event.max_capacity,
        )
        self.db.add(new_event)
        self.db.commit()
        self.db.refresh(new_event)
        return new_event

    def get_all_events(self, target_timezone: str, skip: int = 0, limit: int = 10) -> list:
        """
        Retrieves all upcoming events with pagination.
        """
        events = (
            self.db.query(Event)
            .order_by(Event.start_time)
            .offset(skip)
            .limit(limit)
            .all()
        )
        # Convert to target timezone for output
        for event in events:
            event.start_time = convert_to_timezone(event.start_time, target_timezone)
            event.end_time = convert_to_timezone(event.end_time, target_timezone)

        return events

    def register_attendee(self, event_id: str, attendee: AttendeeRegisterSchema) -> Attendee:
        """
        Registers an attendee for a given event if the event exists and is not full.
        """
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        attendee_count = self.db.query(Attendee).filter(Attendee.event_id == event_id).count()
        if attendee_count >= event.max_capacity:
            raise HTTPException(status_code=400, detail="Event has reached maximum capacity")

        attendee_email = self.db.query(Attendee).filter(Attendee.email == attendee.email,
                                                        Attendee.event_id == event_id).count()
        if attendee_email:
            raise HTTPException(status_code=409, detail="User already exists.")

        new_attendee = Attendee(
            event_id=event_id,
            name=attendee.name,
            email=attendee.email
        )
        self.db.add(new_attendee)
        self.db.commit()
        self.db.refresh(new_attendee)
        return new_attendee

    def get_attendees(self, event_id: str, skip: int = 0, limit: int = 10) -> list[Attendee]:
        """
        Retrieves a paginated list of attendees for a specific event.
        """
        event_exists = self.db.query(Event.id).filter(Event.id == event_id).scalar()
        if not event_exists:
            raise HTTPException(status_code=404, detail="Event not found")

        return (
            self.db.query(Attendee)
            .filter(Attendee.event_id == event_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
