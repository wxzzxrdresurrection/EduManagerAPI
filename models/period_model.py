from pydantic import BaseModel
import datetime

class Period(BaseModel):
    id: str | None = None
    type: str
    start_date: datetime.date
    end_date: datetime.date
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime | None = None
    deleted_at: datetime.datetime | None = None