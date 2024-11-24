from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Project
from uuid import UUID
from app.schemas import AnimatedImageSchema, AnimatedImageUpdate


async def create_project(db_session: AsyncSession, animated_image_schema: AnimatedImageSchema) -> Project:
    project_db = Project(
    )


async def get_project(db_session: AsyncSession, user_id: UUID, project_id: int) -> Project:
    pass


async def delete_project(db_session: AsyncSession, user_id: UUID, project_id: int) -> Project:
    pass


async def update_project(db_session: AsyncSession, user_id: UUID, project_id: int,
                         animated_image_update: AnimatedImageUpdate) -> Project:
    pass
