from pydantic import BaseModel
import datetime

class User(BaseModel):
    id: str
    name: str
    email: str
    password: str
    telephone: str
    created_at: datetime.datetime 
    updated_at: datetime.datetime
    deleted_at: datetime.datetime