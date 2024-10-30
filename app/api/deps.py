from app.core.db import engine
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends, Request, HTTPException, status
import jwt
from app.core.config import settings
from pydantic import ValidationError
from app.crud.users_crud import get_user_by_email
from app.schemas import UserInDB, TokenPayload


async def get_db():
    async with AsyncSession(engine) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(db_session: SessionDep, request: Request) -> UserInDB:
    token = request.cookies.get("token")
    try:
        payload = jwt.decode(
            token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    if token_data.expired:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired"
        )
    user = await get_user_by_email(db_session, token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user


UserDep = Annotated[UserInDB, Depends(get_current_user)]


async def get_current_superuser(user: UserDep) -> UserInDB:
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return user


SuperuserDep = Annotated[UserInDB, Depends(get_current_superuser)]
