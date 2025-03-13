from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .animation import Animation
    from .project import Project


class AnimatedImage(Base, TimestampMixin):
    __tablename__ = "animated_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
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

    project: Mapped["Project"] = relationship(back_populates="animated_images", lazy="selectin")
    animations: Mapped[list["Animation"]] = relationship(back_populates="animated_image", lazy="selectin")
