from fastapi import APIRouter, HTTPException, status
from app.api.deps import SessionDep, UserDep
from app.crud import users_crud
from app.schemas import UserIn, UserOut
from pydantic import EmailStr

router = APIRouter()


@router.get("/me")
async def get_me(user: UserDep) -> UserOut:
    return user


@router.post("/create")
async def create_user(db_session: SessionDep, user_create: UserIn) -> str:
    user = await users_crud.get_user_by_email(db_session, user_create.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )

    await users_crud.create_user(db_session, user_create)
    return "success"


@router.get("/get/{email}")
async def get_user_by_email(db_session: SessionDep, email: EmailStr) -> UserOut:
    user_db = await users_crud.get_user_by_email(db_session, email)
    if user_db:
        return user_db
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/delete/{email}")
async def delete_user_by_email(db_session: SessionDep, email: str) -> UserOut:
    user_db = await users_crud.get_user_by_email(db_session, email)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await users_crud.delete_user(db_session, email)
    return user_db
