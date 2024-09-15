from fastapi import APIRouter
from models.subject_model import Subject
from config.db import MongoConnection

subject = APIRouter()

@subject.get("", response_model=dict)
async def get_all_subjects():
    return {
        "data": [],
        "message": "Subjects retrieved successfully"
    }

@subject.get("/{subject_id}", response_model=Subject)
async def get_subject(subject_id: int):
    return {
        "data": [],
        "message": "Subject retrieved successfully"
    }
