from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .animated_image import AnimatedImage


class Animation(Base, TimestampMixin):
    __tablename__ = "animations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)

    param_name: Mapped[str] = mapped_column(String, nullable=False)
    start_time: Mapped[float] = mapped_column(Float, nullable=False)
    end_time: Mapped[float] = mapped_column(Float, nullable=False)
    start_point: Mapped[float] = mapped_column(Float, nullable=False)
    end_point: Mapped[float] = mapped_column(Float, nullable=False)

    animated_image_id: Mapped[int] = mapped_column(ForeignKey("animated_images.id"), nullable=False)
    animated_image: Mapped["AnimatedImage"] = relationship(back_populates="animations", lazy="selectin")
