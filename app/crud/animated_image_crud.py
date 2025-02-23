from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import AnimatedImage
from app.schemas import AnimatedImageCreate, AnimatedImageUpdate
from default_crud import create_model


async def create_animated_image(
    db_session: AsyncSession, animated_image_create: AnimatedImageCreate
) -> AnimatedImage:
    return await create_model(db_session, animated_image_create, AnimatedImage)


async def get_animated_image(
    db_session: AsyncSession, project_id: int, animated_image_id: int
) -> AnimatedImage | None:
    stmt = select(AnimatedImage).where(
        AnimatedImage.id == animated_image_id, AnimatedImage.project_id == project_id
    )
    animated_image_db = (await db_session.execute(stmt)).first()
    if not animated_image_db:
        return None
    return animated_image_db[0]


async def update_animated_image(
    db_session: AsyncSession,
    project_id: int,
    animated_image_id: int,
    animated_image_update: AnimatedImageUpdate,
) -> AnimatedImage | None:
    animated_image_db = await get_animated_image(
        db_session, project_id, animated_image_id
    )
    if not animated_image_db:
        return None

    for field, value in animated_image_update.model_dump(exclude_unset=True).items():
        setattr(animated_image_db, field, value)

    await db_session.commit()
    await db_session.refresh(animated_image_db)
    return animated_image_db


async def delete_animated_image(
    db_session: AsyncSession, project_id: int, animated_image_id: int
) -> AnimatedImage | None:
    animated_image_db = await get_animated_image(
        db_session, project_id, animated_image_id
    )
    if not animated_image_db:
        return None
    await db_session.delete(animated_image_db)
    await db_session.commit()
    return animated_image_db
