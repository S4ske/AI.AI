from fastapi import APIRouter
from app.api.deps import get_current_user
from app.schemas import ProjectSchema


router = APIRouter()


async def save_project(current_user: get_current_user, project: ProjectSchema) -> bool:
    pass
