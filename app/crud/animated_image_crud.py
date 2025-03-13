from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.animated_image import AnimatedImage
from app.schemas import AnimatedImageCreate, AnimatedImageUpdate


async def create_animated_image(
    db_session: AsyncSession,
    project_id: int,
    animated_image_create: AnimatedImageCreate,
) -> AnimatedImage:
    animated_image_dict = animated_image_create.model_dump()
    animated_image_dict["project_id"] = project_id
    animated_image_db = AnimatedImage(**animated_image_dict)
    db_session.add(animated_image_db)
    await db_session.flush()
    await db_session.refresh(animated_image_db)
    return animated_image_db


async def get_animated_image(
    db_session: AsyncSession, project_id: int, animated_image_id: int
) -> AnimatedImage | None:
    stmt = (
        select(AnimatedImage)
        .where(
            AnimatedImage.id == animated_image_id,
            AnimatedImage.project_id == project_id,
        )
        .options(selectinload(AnimatedImage.animations))
    )
    animated_image_db = (await db_session.execute(stmt)).first()
    if not animated_image_db:
        return None
    return animated_image_db[0]


async def get_animated_images_ids(db_session: AsyncSession, project_id: int) -> None | list[int]:
    stmt = (
        select(AnimatedImage.id)
        .where(AnimatedImage.project_id == project_id)
        .options(selectinload(AnimatedImage.animations))
    )
    return (await db_session.execute(stmt)).first()


async def update_animated_image(
    db_session: AsyncSession,
    project_id: int,
    animated_image_id: int,
    animated_image_update: AnimatedImageUpdate,
) -> AnimatedImage | None:
    animated_image_db = await get_animated_image(db_session, project_id, animated_image_id)
    if not animated_image_db:
        return None

    for field, value in animated_image_update.model_dump(exclude_unset=True).items():
        setattr(animated_image_db, field, value)

    await db_session.flush()
    await db_session.refresh(animated_image_db)
    return animated_image_db


async def delete_animated_image(
    db_session: AsyncSession, project_id: int, animated_image_id: int
) -> AnimatedImage | None:
    animated_image_db = await get_animated_image(db_session, project_id, animated_image_id)
    if not animated_image_db:
        return None
    await db_session.delete(animated_image_db)
    await db_session.flush()
    return animated_image_db
