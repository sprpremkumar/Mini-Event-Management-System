from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from db.database import Base
from utils import generate_id


class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, index=True, default=lambda: generate_id("Event"))
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    max_capacity = Column(Integer, nullable=False)

    attendees = relationship("Attendee", back_populates="event")

class Attendee(Base):
    __tablename__ = "attendees"

    id = Column(String, primary_key=True, index=True, default=lambda: generate_id("Attendee"))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    event_id = Column(String, ForeignKey("events.id"))

    event = relationship("Event", back_populates="attendees")
