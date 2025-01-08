from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from app.rendering.schemas import AnimatedImageParams, AnimationParam


class UserBase(BaseModel):
    email: EmailStr = Field(max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    username: str | None = Field(default=None, max_length=255)


class UserIn(UserBase):
    email: EmailStr = Field(max_length=255)
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


class AnimationSchema(BaseModel):
    param_name: AnimationParam
    start_time: float
    end_time: float
    start_point: float
    end_point: float


class AnimatedImageSchema(BaseModel):
    name: str
    living_start: float
    living_end: float
    params: AnimatedImageParams
    animations: list[AnimationSchema]


class AnimatedImageUpdate(BaseModel):
    id: int
    height: int | None = None
    width: int | None = None
    angle: float | None = None
    opacity: float | None = None
    x: float | None = None
    y: float | None = None
    living_start: float | None = None
    living_end: float | None = None
    project_id: int
    animations: list[AnimationSchema] | None


class ProjectSchema(BaseModel):
    animated_images: list[AnimatedImageSchema]
    name: str
    duration: float = Field(gt=0)
    shape: tuple[int, int] = Field(gt=(0, 0))
    background_color: tuple[int, int, int]
    fps: int = Field(gt=0)
