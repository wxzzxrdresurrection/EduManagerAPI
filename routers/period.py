from fastapi import APIRouter
from schemas.period import PeriodSchema
from models.period_model import Period

periods = APIRouter()

@periods.get("", status_code=200)
def get_periods():
    periods = PeriodSchema().get_all_periods()
    return {
        "data": periods,
        "message": "Periods retrieved successfully"
    }

@periods.get("/{period_id}", status_code=200)
def get_period(period_id: str):
    period = PeriodSchema().get_period(period_id)
    return {
        "data": period,
        "message": "Period retrieved successfully"
    }

@periods.post("", status_code=201)
def create_period(period: Period):
    data = PeriodSchema().add_period(period)
    return {
        "data": data,
        "message": "Period created successfully"
   }
