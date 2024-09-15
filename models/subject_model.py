from pydantic import BaseModel
import datetime

class Subject(BaseModel):
<<<<<<< HEAD
<<<<<<< HEAD
    id: int
=======
    id: str | None = None
>>>>>>> c141412 (feat: :sparkles: added subjects create, read all and read one by id)
=======
    id: str | None = None
>>>>>>> upstream/zapataLuis
    name: str
    description: str
    units: list
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime | None = None
    deleted_at: datetime.datetime | None = None