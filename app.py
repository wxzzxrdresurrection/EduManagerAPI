from fastapi import FastAPI
from routers.subject import subjects

app = FastAPI(
    title="EduManagerAPI",
    description="This is a detailed description of my API.",
    version="1.0.0")

app.include_router(subjects, prefix="/subject", tags=["subject"])
