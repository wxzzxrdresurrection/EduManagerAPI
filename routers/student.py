from fastapi import APIRouter
from schemas.student import StudentSchema
from models.student_model import Student

students = APIRouter()

@students.post("", response_model=dict, status_code=201)
async def create_student(student: Student):
    data = StudentSchema().add_student(student)
    return {
        "data": data,
        "message": "Student created successfully"
    }

@students.get("", response_model=dict, status_code=200)
async def get_students():
    students = StudentSchema().get_students()
    return {
        "data": students,
        "message": "Students retrieved successfully"
    }

@students.get("/{student_id}", response_model=dict, status_code=200)
async def get_student(student_id: str):
    student = StudentSchema().get_student(student_id)
    return {
        "data": student,
        "message": "Student retrieved successfully"
    }