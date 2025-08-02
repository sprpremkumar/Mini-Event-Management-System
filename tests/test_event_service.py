import unittest
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.database import Base, engine
from models.event import Attendee
from schemas.event_schema import AttendeeRegisterSchema, EventCreationSchema
from services.event_service import EventService
from utils import generate_id

# Setup DB schema for testing
Base.metadata.create_all(bind=engine)


class TestEventService(unittest.TestCase):

    def create_event(self):
        # Shared setup: create event for use across test cases
        start = datetime.now(timezone.utc) + timedelta(hours=1)
        end = start + timedelta(hours=1)

        schema = EventCreationSchema(
            name="Conference",
            location="Remote",
            start_time=start,
            end_time=end,
            max_capacity=50
        )
        self.event = self.service.create_event(schema)
        self.event_id = self.event.id
        self.start_time = start
        self.end_time = end

    def setUp(self):
        # Use an in-memory SQLite database
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.db = self.Session()
        self.service = EventService(self.db)
        self.create_event()


    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(bind=self.engine)

    def test_event_created_in_setup(self):
        self.assertIsNotNone(self.event_id)
        self.assertEqual(self.event.name, "Conference")
        self.assertEqual(self.event.start_time, self.start_time.replace(tzinfo=None))

    def test_get_all_events(self):
        events = self.service.get_all_events("Asia/Kolkata")

        self.assertEqual(len(events), 1)
        for e in events:
            self.assertEqual(e.location, "Remote")
            self.assertIn("Asia", str(e.start_time.tzinfo))  # confirm converted

    def test_get_all_events_with_pagination(self):
        events = self.service.get_all_events("Asia/Kolkata", skip=0, limit=10)
        self.assertEqual(len(events), 1)



    def test_register_attendee_success(self):
        data = AttendeeRegisterSchema(name="Alice", email="alice@example.com")
        attendee = self.service.register_attendee(self.event_id, data)
        self.assertEqual(attendee.name, "Alice")
        self.assertEqual(attendee.email, "alice@example.com")

    def test_event_not_found(self):
        data = AttendeeRegisterSchema(name="Bob", email="bob@example.com")
        with self.assertRaises(HTTPException) as context:
            self.service.register_attendee(event_id="9999", attendee=data)
        self.assertEqual(context.exception.status_code, 404)
        self.assertIn("Event not found", context.exception.detail)

    def test_event_capacity_reached(self):
        # Fill event to capacity
        for i in range(50):
            self.db.add(
                Attendee(id=generate_id("Attendee"), name=f"User{i}", email=f"u{i}@example.com", event_id=self.event_id),
            )
            self.db.commit()

        data = AttendeeRegisterSchema(name="Charlie", email="charlie@example.com")
        with self.assertRaises(HTTPException) as context:
            self.service.register_attendee(self.event_id, data)
        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("Event has reached maximum capacity", context.exception.detail)

    def test_duplicate_attendee(self):
        self.db.add(Attendee(name="Dave", email="dave@example.com", event_id=self.event_id))
        self.db.commit()

        data = AttendeeRegisterSchema(name="Dave", email="dave@example.com")
        with self.assertRaises(HTTPException) as context:
            self.service.register_attendee(self.event_id, data)
        self.assertEqual(context.exception.status_code, 409)
        self.assertIn("User already exists.", context.exception.detail)


if __name__ == "__main__":
    unittest.main()
