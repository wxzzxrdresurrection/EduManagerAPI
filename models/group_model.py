from pydantic import BaseModel
import datetime

class Group(BaseModel):
    id: int
    number: str
    letter: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime