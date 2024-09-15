from pydantic import BaseModel
import datetime

class Group(BaseModel):
    id: str | None = None
    number: str
    letter: str
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime | None = None
    deleted_at: datetime.datetime | None = None