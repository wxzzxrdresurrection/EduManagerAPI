from fastapi import APIRouter
from models.schedule_model import Schedule
from schemas.schedule import ScheduleSchema

schedules = APIRouter()

@schedules.get("", response_model=dict, status_code=200)
async def get_all_schedules():
    schedules = ScheduleSchema().get_all_schedules()
    return {
        "data": schedules,
        "message": "Schedules retrieved successfully"
    }


@schedules.get("/{schedule_id}", response_model=dict, status_code=200)
async def get_schedule(schedule_id: str):
    schedule = ScheduleSchema().get_schedule(schedule_id)
    return {
        "data": schedule,
        "message": "Schedule retrieved successfully"
    }


@schedules.post("", response_model=dict, status_code=201)
async def add_schedule(schedule: Schedule):
    data = ScheduleSchema().add_schedule(schedule)
    return {
        "data": data,
        "message": "Schedule added successfully"
    }

@schedules.get("/group/{group_id}", response_model=dict, status_code=200)
async def get_schedule_by_group(group_id: str):
    schedules = ScheduleSchema().get_schedule_by_group(group_id)
    return {
        "data": schedules,
        "message": "Schedules retrieved successfully"
    }