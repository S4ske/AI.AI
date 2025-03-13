from fastapi import APIRouter, HTTPException, status
from pydantic import EmailStr

from app.api.deps import SessionDepWithCommit, UserDep
from app.crud import users_crud
from app.schemas import UserIn, UserOut

router = APIRouter()


@router.get("/me")
async def get_me(user: UserDep) -> UserOut:
    return user


@router.post("/create")
async def create_user(db_session: SessionDepWithCommit, user_create: UserIn) -> UserOut:
    user = await users_crud.get_user_by_email(db_session, user_create.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )

    user = await users_crud.create_user(db_session, user_create)
    return user


@router.get("/get/{email}")
async def get_user_by_email(db_session: SessionDepWithCommit, email: EmailStr) -> UserOut:
    user_db = await users_crud.get_user_by_email(db_session, email)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user_db


@router.post("/delete/{email}")
async def delete_user_by_email(db_session: SessionDepWithCommit, email: str) -> UserOut:
    user_db = await users_crud.delete_user(db_session, email)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user_db
