from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.rendering.schemas import AnimationParam


class TimestampSchema(BaseModel):
    created_at: datetime
    updated_at: datetime


class UserBase(BaseModel):
    email: EmailStr = Field(max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    username: str | None = Field(default=None, max_length=255)


class UserSchema(TimestampSchema):
    id: UUID
    email: str
    username: str | None
    hashed_password: str
    is_active: bool
    is_superuser: bool
    projects: list["ProjectSchema"]


class UserIn(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserOut(UserBase):
    id: UUID

    class Config:
        from_attributes = True


class UserInDB(UserBase):
    id: UUID
    hashed_password: str


class TokenPayload(BaseModel):
    sub: str


class AnimationSchema(TimestampSchema):
    id: int
    param_name: AnimationParam
    start_time: float
    end_time: float
    start_point: float
    end_point: float
    animated_image_id: int


class AnimationCreate(BaseModel):
    param_name: AnimationParam
    start_time: float
    end_time: float
    start_point: float
    end_point: float


class AnimationUpdate(BaseModel):
    param_name: AnimationParam | None = None
    start_time: float | None = None
    end_time: float | None = None
    start_point: float | None = None
    end_point: float | None = None


class AnimatedImageSchema(TimestampSchema):
    id: int
    image_path: str
    height: int
    width: int
    angle: float
    opacity: float
    x: float
    y: float
    living_start: float
    living_end: float
    project_id: int
    animations: list[AnimationSchema]


class AnimatedImageCreate(BaseModel):
    image_path: str
    height: int
    width: int
    angle: float
    opacity: float
    x: float
    y: float
    living_start: float
    living_end: float


class AnimatedImageUpdate(BaseModel):
    image_path: str | None = None
    height: int | None = None
    width: int | None = None
    angle: float | None = None
    opacity: float | None = None
    x: float | None = None
    y: float | None = None
    living_start: float | None = None
    living_end: float | None = None


class ProjectSchema(TimestampSchema):
    id: int
    name: str = Field(max_length=255)
    height: int = Field(ge=0)
    width: int = Field(ge=0)
    fps: int = Field(ge=0)
    duration: float = Field(ge=0)
    background_color: tuple[int, int, int]
    owner_id: UUID
    animated_images: list[AnimatedImageSchema]


class ProjectCreate(BaseModel):
    name: str = Field(max_length=255)
    height: int = Field(ge=0)
    width: int = Field(ge=0)
    fps: int = Field(ge=0)
    duration: float = Field(ge=0)
    background_color: tuple[int, int, int]


class ProjectUpdate(BaseModel):
    name: str | None = Field(max_length=255, default=None)
    height: int | None = Field(ge=0, default=None)
    width: int | None = Field(ge=0, default=None)
    fps: int | None = Field(ge=0, default=None)
    duration: float | None = Field(ge=0, default=None)
    background_color: tuple[int, int, int] | None = Field(default=None)
