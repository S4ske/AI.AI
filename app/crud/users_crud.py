from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.schemas import UserIn
from app.core.security import get_password_hash, verify_password
from uuid import UUID
from sqlalchemy import select


async def create_user(db_session: AsyncSession, user_create: UserIn) -> User:
    user_db = User(
        username=user_create.username,
        email=user_create.email,
        is_active=user_create.is_active,
        is_superuser=user_create.is_superuser,
        hashed_password=get_password_hash(user_create.password),
    )
    db_session.add(user_db)
    await db_session.commit()
    await db_session.refresh(user_db)
    return user_db


async def get_user_by_id(db_session: AsyncSession, id: UUID) -> User | None:
    stmt = select(User).where(User.id == id)
    result = await db_session.execute(stmt)
    if not result:
        return None
    user_db = result.first()
    if not user_db:
        return None
    return user_db[0]


async def get_user_by_username(db_session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await db_session.execute(stmt)
    if not result:
        return None
    user_db = result.first()
    if not user_db:
        return None
    return user_db[0]


async def get_user_by_email(db_session: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await db_session.execute(stmt)
    user_db = result.first()
    if not user_db:
        return None
    return user_db[0]


async def authenticate(
    db_session: AsyncSession, username: str, password: str
) -> User | None:
    user = await get_user_by_email(db_session, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def delete_user(db_session: AsyncSession, email: str) -> User | None:
    user_db = await get_user_by_email(db_session, email)
    if not user_db:
        return None
    await db_session.delete(user_db)
    await db_session.commit()
    return user_db


async def update_user(
    db_session: AsyncSession, id: UUID, user_update: UserIn
) -> User | None:
    user_data = user_update.model_dump(exclude_unset=True)
    user_db = await get_user_by_id(db_session, id)
    if not user_db:
        return None

    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        user_data["hashed_password"] = hashed_password

    for field, value in user_data.items():
        setattr(user_db, field, value)

    await db_session.commit()
    await db_session.refresh(user_db)
    return user_db
