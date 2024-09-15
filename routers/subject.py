from fastapi import APIRouter
from models.subject_model import Subject
from schemas.subject import SubjectSchema
from routers.ws import llm

subjects = APIRouter()

@subjects.get("", response_model=dict, status_code=200)
async def get_all_subjects():
    subjects = SubjectSchema().get_subjects()
    return {
        "data": subjects,
        "message": "Subjects retrieved successfully"
    }

@subjects.get("/{subject_id}", response_model=dict, status_code=200)
async def get_subject(subject_id: str):
    subject = SubjectSchema().get_subject(subject_id)
    return {
        "data": subject,
        "message": "Subject retrieved successfully"
    }

@subjects.post("", response_model=dict,status_code=201)
async def add_subject(subject: Subject):
    new_subject = SubjectSchema().add_subject(subject)
    return {
        "data": new_subject,
        "message": "Subject added successfully"
    }

@subjects.get("/{subject_id}/students", response_model=dict)
async def get_students(subject_id: str):
    structure = {
        "id":"string",
        "name": "string",
        "psicological_state": "Muy bueno| Promedio | Necesita atención",
        "grade_average": "float one to ten",
        "assistance_average": "float one to ten",
    }
    students = await llm.generate_response_sync(f"bring all students with the next structure: {str(structure)}")
    return {
        "data": students,
        "message": "Students retrieved successfully"
    }
