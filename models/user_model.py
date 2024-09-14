from pydantic import BaseModel
import datetime

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
    telephone: str
    created_at: datetime.datetime 
    updated_at: datetime.datetime
    deleted_at: datetime.datetime