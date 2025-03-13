from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import SessionDepWithCommit
from app.core.security import create_access_token, verify_password
from app.crud import users_crud

router = APIRouter()


@router.post("/login")
async def login(
    db_session: SessionDepWithCommit,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
) -> str:
    user = await users_crud.get_user_by_email(db_session, form.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong email")
    if not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password")
    token = create_access_token(user.email, expires_delta=timedelta(days=7))
    response.set_cookie(
        key="token",
        value=token,
        max_age=int(timedelta(days=7).total_seconds()),
        httponly=True,
        secure=False,  # TODO: Передать True, когда перейдём на HTTPS
    )
    return "success"


@router.get("/logout")
async def logout(response: Response) -> str:
    response.delete_cookie("token")
    return "success"
