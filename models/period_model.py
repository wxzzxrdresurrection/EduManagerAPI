from pydantic import BaseModel
import datetime

class Period(BaseModel):
    id: int
    type: str
    start_date: datetime.date
    end_date: datetime.date
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime