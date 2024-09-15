from pydantic import BaseModel
import datetime

class Attendance(BaseModel):
    id: str | None = None
    student_list: list
    subject_id: str
    group_id: str
    teacher_id: str
    day: datetime.date
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime | None = None
    deleted_at: datetime.datetime | None = None