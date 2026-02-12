from datetime import date, datetime, time
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator, model_validator


class AttendanceBase(BaseModel):
    employee_id: int
    work_date: date
    time_in: Optional[time] = None
    time_out: Optional[time] = None
    status: str = "PRESENT"


class AttendanceResponse(AttendanceBase):
    id: int
    minutes_late: int
    minutes_undertime: int
    overtime_hours: float
    model_config = ConfigDict(from_attributes=True)

    @field_validator("time_in", mode="before")
    @classmethod
    def parse_iso_string(cls, v):
        if isinstance(v, str):
            dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
            return dt.time().replace(tzinfo=None)
        return v


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(BaseModel):
    time_out: time

    # Re-use your time parser to handle ISO strings/Zulu format
    @field_validator("time_out", mode="before")
    @classmethod
    def parse_time_properly(cls, v):
        if isinstance(v, str):
            try:
                return time.fromisoformat(v)
            except ValueError:
                v = v.replace("Z", "+00:00")
                return datetime.fromisoformat(v).time().replace(tzinfo=None)
        return v
