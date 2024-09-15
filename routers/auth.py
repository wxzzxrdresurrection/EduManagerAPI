from fastapi import APIRouter
from schemas.user import UserSchema
from models.user_model import UserLogin

auth = APIRouter()

@auth.post("/login", response_model=dict, status_code=200)
async def login(user: UserLogin):
    info = UserSchema().login(user)
    return {
        "data": info,
        "message": "Login successful"
    }