from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Animation
from app.schemas import AnimationCreate, AnimationUpdate
from default_crud import create_model
from sqlalchemy import select


async def create_animation(
    db_session: AsyncSession, animation_create: AnimationCreate
) -> Animation:
    return await create_model(db_session, animation_create, Animation)


async def get_animation(
    db_session: AsyncSession, animated_image_id: int, animation_id: int
) -> Animation | None:
    stmt = select(Animation).where(
        Animation.id == animation_id, Animation.animated_image_id == animated_image_id
    )
    animation_db = (await db_session.execute(stmt)).first()
    if not animation_db:
        return None
    return animation_db[0]


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

    await db_session.commit()
    await db_session.refresh(animation_db)
    return animation_db


async def delete_animation(
    db_session: AsyncSession, animated_image_id: int, animation_id: int
) -> Animation | None:
    animation_db = await get_animation(db_session, animated_image_id, animation_id)
    if not animation_db:
        return None
    await db_session.delete(animation_db)
    await db_session.commit()
    return animation_db
