from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.project import Project
from app.schemas import ProjectCreate, ProjectUpdate


async def create_project(db_session: AsyncSession, owner_id: UUID, project_create: ProjectCreate) -> Project:
    project_dict = project_create.model_dump()
    project_dict["owner_id"] = owner_id
    project_db = Project(**project_dict)
    db_session.add(project_db)
    await db_session.flush()
    await db_session.refresh(project_db)
    return project_db


async def get_project(db_session: AsyncSession, user_id: UUID, project_id: int) -> Project | None:
    stmt = (
        select(Project)
        .where(Project.id == project_id, Project.owner_id == user_id)
        .options(selectinload(Project.animated_images))
    )
    project_db = (await db_session.execute(stmt)).first()
    if not project_db:
        return None
    return project_db[0]


async def get_project_ids(db_session: AsyncSession, user_id: UUID) -> list[int]:
    stmt = select(Project.id).where(Project.owner_id == user_id)
    return list((await db_session.execute(stmt)).scalars())


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

    await db_session.flush()
    await db_session.refresh(project_db)
    return project_db


async def delete_project(db_session: AsyncSession, user_id: UUID, project_id: int) -> Project | None:
    project_db = await get_project(db_session, user_id, project_id)
    if not project_db:
        return None
    await db_session.delete(project_db)
    await db_session.flush()
    return project_db
