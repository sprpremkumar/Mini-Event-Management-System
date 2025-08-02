import uuid
from datetime import datetime, timezone

from pytz import timezone as py_timezone


def convert_to_timezone(dt: datetime, tz_str: str) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    target_tz = py_timezone(tz_str)
    return dt.astimezone(target_tz)

def generate_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"

def to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
