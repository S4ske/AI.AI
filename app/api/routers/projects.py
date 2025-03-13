from fastapi import APIRouter, HTTPException, status

from app.api.deps import SessionDepWithCommit, UserDep
from app.crud import projects_crud
from app.schemas import ProjectCreate, ProjectSchema, ProjectUpdate

router = APIRouter()


@router.post("/create_raw")
async def create_raw_project(
    db_session: SessionDepWithCommit, user: UserDep, project_schema: ProjectCreate
) -> ProjectSchema:
    project_db = await projects_crud.create_project(db_session, user.id, project_schema)
    if not project_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return project_db


@router.get("/get/{project_id}")
async def get_project(db_session: SessionDepWithCommit, user: UserDep, project_id: int) -> ProjectSchema:
    project_db = await projects_crud.get_project(db_session, user.id, project_id)
    if not project_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return project_db


@router.get("/get_ids")
async def get_projects_ids(db_session: SessionDepWithCommit, user: UserDep) -> list[int]:
    projects_ids = await projects_crud.get_project_ids(db_session, user.id)
    if not projects_ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return projects_ids


@router.put("update/{project_id}")
async def update_project(
    db_session: SessionDepWithCommit,
    user: UserDep,
    project_id: int,
    project_update: ProjectUpdate,
) -> ProjectSchema:
    project_db = await projects_crud.update_project(db_session, user.id, project_id, project_update)
    if not project_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return project_db


@router.delete("delete/{project_id}")
async def delete_project(db_session: SessionDepWithCommit, user: UserDep, project_id: int) -> ProjectSchema:
    project_db = await projects_crud.delete_project(db_session, user.id, project_id)
    if not project_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return project_db
