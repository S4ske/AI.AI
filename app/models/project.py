from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ARRAY, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .animated_image import AnimatedImage
    from .user import User


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    fps: Mapped[int] = mapped_column(Integer, nullable=False, default=20)
    duration: Mapped[float] = mapped_column(Float, nullable=False)
    background_color: Mapped[tuple[int, int, int]] = mapped_column(ARRAY(Integer), nullable=False)

    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    animated_images: Mapped[list["AnimatedImage"]] = relationship(back_populates="project", lazy="selectin")
    owner: Mapped["User"] = relationship(back_populates="projects", lazy="selectin")
