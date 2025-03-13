from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.animation import Animation
from app.schemas import AnimationCreate, AnimationUpdate


async def create_animation(
    db_session: AsyncSession, animated_image_id: int, animation_create: AnimationCreate
) -> Animation:
    animation_dict = animation_create.model_dump()
    animation_dict["animated_image_id"] = animated_image_id
    animation_db = Animation(**animation_dict)
    db_session.add(animation_db)
    await db_session.flush()
    await db_session.refresh(animation_db)
    return animation_db


async def get_animation(db_session: AsyncSession, animated_image_id: int, animation_id: int) -> Animation | None:
    stmt = select(Animation).where(Animation.id == animation_id, Animation.animated_image_id == animated_image_id)
    animation_db = (await db_session.execute(stmt)).first()
    if not animation_db:
        return None
    return animation_db[0]


async def get_animations_ids(db_session: AsyncSession, animated_image_id: int) -> None | list[int]:
    stmt = select(Animation.id).where(Animation.animated_image_ids == animated_image_id)
    return (await db_session.execute(stmt)).first()


async def update_animation(
    db_session: AsyncSession,
    animated_image_id: int,
    animation_id: int,
    animation_update: AnimationUpdate,
) -> Animation | None:
    animation_db = await get_animation(db_session, animated_image_id, animation_id)
    if not animation_db:
        return None

    animation_data = animation_update.model_dump(exclude_unset=True)
    for field, value in animation_data.items():
        setattr(animation_db, field, value)

    await db_session.flush()
    await db_session.refresh(animation_db)
    return animation_db


async def delete_animation(db_session: AsyncSession, animated_image_id: int, animation_id: int) -> Animation | None:
    animation_db = await get_animation(db_session, animated_image_id, animation_id)
    if not animation_db:
        return None
    await db_session.delete(animation_db)
    await db_session.flush()
    return animation_db
