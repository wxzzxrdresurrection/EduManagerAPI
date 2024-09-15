from pydantic import BaseModel
import datetime

class Student(BaseModel):
    id: str | None = None
    first_name: str
    middle_name: str
    last_name: str
    age: str
    email: str
    telephone: str
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime | None = None
    deleted_at: datetime.datetime | None = None