from pydantic import BaseModel
import datetime

class Subject(BaseModel):
    id: str | None = None
    name: str
    description: str
    units: list
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime | None = None
    deleted_at: datetime.datetime | None = None
