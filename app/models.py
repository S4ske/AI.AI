from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Integer,
    ForeignKey,
    Float,
    TupleType,
    func,
)
from datetime import datetime
from uuid import uuid4, UUID

Base = declarative_base()


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False
    )


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    username: Mapped[str | None] = mapped_column(
        String(length=255), default=None, nullable=True
    )
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    projects: Mapped[list["Project"]] = relationship(back_populates="owner")


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    fps: Mapped[int] = mapped_column(Integer, nullable=False, default=20)
    duration: Mapped[float] = mapped_column(Float, nullable=False)
    background_color: Mapped[tuple[int, int, int]] = mapped_column(
        TupleType(Integer, Integer, Integer), nullable=False
    )

    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    animated_images: Mapped[list["AnimatedImage"]] = relationship(
        back_populates="project"
    )
    owner: Mapped[User] = relationship(back_populates="projects")


class AnimatedImage(Base, TimestampMixin):
    __tablename__ = "animated_images"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    image_path: Mapped[str] = mapped_column(String, nullable=False)

    height: Mapped[int] = mapped_column(Integer, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    angle: Mapped[float] = mapped_column(Float, nullable=False)
    opacity: Mapped[float] = mapped_column(Float, nullable=False)
    x: Mapped[float] = mapped_column(Float, nullable=False)
    y: Mapped[float] = mapped_column(Float, nullable=False)
    living_start: Mapped[float] = mapped_column(Float, nullable=False)
    living_end: Mapped[float] = mapped_column(Float, nullable=False)

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)

    project: Mapped[Project] = relationship(back_populates="animated_images")
    animations: Mapped[list["Animation"]] = relationship(
        back_populates="animated_image"
    )


class Animation(Base, TimestampMixin):
    __tablename__ = "animations"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )

    param_name: Mapped[str] = mapped_column(String, nullable=False)
    start_time: Mapped[float] = mapped_column(Float, nullable=False)
    end_time: Mapped[float] = mapped_column(Float, nullable=False)
    start_point: Mapped[float] = mapped_column(Float, nullable=False)
    end_point: Mapped[float] = mapped_column(Float, nullable=False)

    animated_image_id: Mapped[int] = mapped_column(
        ForeignKey("animated_images.id"), nullable=False
    )
    animated_image: Mapped[AnimatedImage] = relationship(back_populates="animations")
