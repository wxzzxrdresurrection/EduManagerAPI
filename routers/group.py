from fastapi import APIRouter
from models.group_model import Group
from schemas.group import GroupSchema

groups = APIRouter()

@groups.get("", response_model=dict, status_code=200)
async def get_all_groups():
    groups = GroupSchema().get_groups()
    return {
        "data": groups,
        "message": "Groups retrieved successfully"
    }

@groups.get("/{group_id}", response_model=dict, status_code=200)
async def get_group(group_id: str):
    group = GroupSchema().get_group(group_id)
    return {
        "data": group,
        "message": "Group retrieved successfully"
    }

@groups.post("", response_model=dict, status_code=201)
async def add_group(group: Group):
    data = GroupSchema().add_group(group)
    return {
        "data": data,
        "message": "Group added successfully"
    }
