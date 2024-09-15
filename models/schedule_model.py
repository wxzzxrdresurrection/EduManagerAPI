from pydantic import BaseModel
import datetime
class Schedule(BaseModel):
    id: str | None
    group_id: str
    subject_id: str
    day: str
    start_time: datetime.date
    end_time: datetime.date
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime | None = None
    deleted_at: datetime.datetime | None = None