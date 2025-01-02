from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Project
from uuid import UUID
from app.schemas import ProjectSchema, ProjectUpdate


async def create_project(
    db_session: AsyncSession, project_schema: ProjectSchema
) -> Project:
    pass


async def get_project(
    db_session: AsyncSession, user_id: UUID, project_id: int
) -> Project:
    pass


async def delete_project(
    db_session: AsyncSession, user_id: UUID, project_id: int
) -> Project:
    pass


async def update_project(
    db_session: AsyncSession,
    user_id: UUID,
    project_id: int,
    project_update: ProjectUpdate,
) -> Project:
    pass
