from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.database import Base, engine
from routes.events import event_router

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Event Management System",
    description="Create events, register attendees, and view attendees per event",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(event_router, prefix="/events", tags=["Events"])
