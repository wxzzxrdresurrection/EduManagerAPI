from pydantic import BaseModel
import datetime

class Role(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime