from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Project
from uuid import UUID
from app.schemas import ProjectCreate, ProjectUpdate
from default_crud import create_model


async def create_project(
    db_session: AsyncSession, project_create: ProjectCreate
) -> Project:
    return await create_model(db_session, project_create, Project)


async def get_project(
    db_session: AsyncSession, user_id: UUID, project_id: int
) -> Project | None:
    stmt = select(Project).where(Project.id == project_id, Project.owner_id == user_id)
    project_db = (await db_session.execute(stmt)).first()
    if not project_db:
        return None
    return project_db[0]


async def update_project(
    db_session: AsyncSession,
    user_id: UUID,
    project_id: int,
    project_update: ProjectUpdate,
) -> Project | None:
    project_db = await get_project(db_session, user_id, project_id)
    if not project_db:
        return None

    for field, value in project_update.model_dump(exclude_unset=True).items():
        setattr(project_db, field, value)

    await db_session.commit()
    await db_session.refresh(project_db)
    return project_db


async def delete_project(
    db_session: AsyncSession, user_id: UUID, project_id: int
) -> Project | None:
    project_db = await get_project(db_session, user_id, project_id)
    if not project_db:
        return None
    await db_session.delete(project_db)
    await db_session.commit()
    return project_db
