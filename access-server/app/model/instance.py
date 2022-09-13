from datetime import datetime, timezone
from pydantic import BaseModel, validator
from typing import Optional

def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

def transform_to_utc_datetime(dt: datetime) -> datetime:
    return dt.astimezone(tz=timezone.utc)

class Instance(BaseModel):
    id: Optional[int] = None
    path: str
    start_date: datetime
    end_date: datetime
    user_token: str
    ssh_user: str
    ssh_pass: str
    ssh_port: str

    # custom input conversion for that field
    _normalize_datetimes = validator(
        "start_date", "end_date",
        allow_reuse=True)(transform_to_utc_datetime)

    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }
    