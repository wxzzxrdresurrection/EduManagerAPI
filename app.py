from fastapi import FastAPI
from routers.subject import subject

app = FastAPI(
    title="EduManagerAPI",
    description="This is a detailed description of my API.",
    version="1.0.0")

app.include_router(subject, prefix="/subject", tags=["subject"])
