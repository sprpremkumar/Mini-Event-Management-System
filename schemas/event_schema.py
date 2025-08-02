from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

class EventSchema(BaseModel):
    class Config:
        extra = "forbid"
        orm_mode = True

class EventCreationSchema(EventSchema):
    name: str = Field(min_length=1, max_length=100, description="Event name")
    location: str = Field(min_length=1, max_length=250, description="Event location")
    start_time: datetime = Field(description="Event start time")
    end_time: datetime = Field(description="Event end time")
    max_capacity: int = Field(ge=10, description="Event maximum capacity")

class AttendeeRegisterSchema(EventSchema):
    name: str = Field(min_length=1, max_length=100, description="Name of the attendee")
    email: EmailStr | str = Field(description="Email address")

class EventResponseSchema(EventSchema):
    id: str
    name: str
    location: str
    start_time: datetime
    end_time: datetime
    max_capacity: int

class AttendeeResponseSchema(EventSchema):
    id: str
    name: str
    email: EmailStr
