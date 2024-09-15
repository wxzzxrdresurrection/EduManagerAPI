from fastapi import APIRouter
from models.attendance_model import Attendance
from schemas.attendance import AttendanceSchema

attendances = APIRouter()

@attendances.get("", response_model=dict, status_code=200)
async def get_all_attendance():
    attendance = AttendanceSchema().get_all_attendance()
    return {
        "data": attendance,
        "message": "Attendance retrieved successfully"
    }

@attendances.get("/{att_id}", response_model=dict, status_code=200)
async def get_attendance(att_id: str):
    att = AttendanceSchema().get_attendance(att_id)
    return {
        "data": att,
        "message": "Attendance retrieved successfully"
    }

@attendances.post("", response_model=dict, status_code=201)
async def add_attendance(att: Attendance):
    data = AttendanceSchema().add_attendance(att)
    return {
        "data": data,
        "message": "Attendance added successfully"
   }

@attendances.get("/group/{group_id}", response_model=dict, status_code=200)
async def get_attendance_by_group(group_id: str):
    att = AttendanceSchema().get_attendance_by_group(group_id)
    return {
        "data": att,
        "message": "Attendance retrieved successfully"
    }