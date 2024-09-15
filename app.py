from fastapi import FastAPI
from routers.subject import subjects
from routers.user import users
from routers.auth import auth

app = FastAPI(
    title="EduManagerAPI",
    description="This is a detailed description of my API.",
    version="1.0.0")

app.include_router(subjects, prefix="/subject", tags=["subject"])
app.include_router(users, prefix="/user", tags=["user"])
app.include_router(auth, prefix="/auth", tags=["auth"])