from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Project


async def create_project(db_session: AsyncSession) -> Project:
    pass


async def get_project(db_session: AsyncSession) -> Project:
    pass


async def delete_project(db_session: AsyncSession) -> Project:
    pass


async def update_project(db_session: AsyncSession) -> Project:
    pass
