from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime, timezone


class UserBase(BaseModel):
    email: EmailStr = Field(max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    username: str | None = Field(default=None, max_length=255)


class UserIn(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str | None = Field(min_length=8, max_length=40, default=None)


class UserOut(UserBase):
    id: UUID

    class Config:
        from_attributes = True


class UserInDB(UserBase):
    id: UUID
    hashed_password: str | None = None


class TokenPayload(BaseModel):
    sub: str | None = None
    exp: datetime

    def expired(self) -> bool:
        return self.exp <= datetime.now(timezone.utc)
