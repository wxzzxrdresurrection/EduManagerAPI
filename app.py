from dotenv import load_dotenv
load_dotenv()

from fastapi.middleware.cors import CORSMiddleware
from routers.ws import ws_router
from fastapi import FastAPI
from routers.subject import subjects
from routers.user import users
from routers.auth import auth
from routers.student import students
from routers.period import periods
from routers.group import groups
from routers.schedule import schedules
from routers.attendance import attendances

app = FastAPI(
    title="EduManagerAPI",
    description="This is a detailed description of my API.",
    version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(subjects, prefix="/subject", tags=["subject"])
app.include_router(users, prefix="/user", tags=["user"])
app.include_router(auth, prefix="/auth", tags=["auth"])
app.include_router(ws_router, prefix="/ws", tags=["ws"])
app.include_router(students, prefix="/student", tags=["student"])
app.include_router(periods, prefix="/period", tags=["period"])
app.include_router(groups, prefix="/group", tags=["group"])
app.include_router(schedules, prefix="/schedule", tags=["schedule"])
app.include_router(attendances, prefix="/attendance", tags=["attendance"])

