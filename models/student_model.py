from pydantic import BaseModel
import datetime

class Student(BaseModel):
    id: str
    first_name: str
    middle_name: str
    last_name: str
    age: str
    email: str
    telephone: str
    created_at: datetime.datetime 
    updated_at: datetime.datetime
    deleted_at: datetime.datetime