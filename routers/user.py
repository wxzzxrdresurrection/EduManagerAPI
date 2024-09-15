from fastapi import APIRouter
from models.user_model import User
from models.user_model import get_password_hash
from schemas.user import UserSchema

users = APIRouter()

@users.get("", response_model=dict, status_code=200)
async def get_all_users():
    users = UserSchema().get_users()
    return {
        "data": users,
        "message": "Users retrieved successfully"
    }

@users.get("/{user_id}", response_model=dict, status_code=200)
async def get_user(user_id: str):
    user = UserSchema().get_user(user_id)
    return {
        "data": user,
        "message": "User retrieved successfully"
    }

@users.post("", response_model=dict, status_code=201)
async def add_user(user: User):
    user.password = get_password_hash(user.password)
    new_user = UserSchema().add_user(user)
    return {
        "data": new_user,
        "message": "User added successfully"
    }
