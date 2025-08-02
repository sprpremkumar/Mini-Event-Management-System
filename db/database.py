from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = "sqlite:///./event.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

EventSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for model declarations
Base = declarative_base()

# Dependency to get a DB session
def get_db() -> Session:
    db = EventSession()
    try:
        yield db
    finally:
        db.close()
