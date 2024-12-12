from pydantic import BaseModel, Field
from enum import Enum


class AnimationParam(Enum):
    x = "x"
    y = "y"
    angle = "angle"
    opacity = "opacity"
    scale_x = "scale_x"
    scale_y = "scale_y"


class AnimatedImageParams(BaseModel):
    x: float
    y: float
    angle: float
    opacity: float
    scale_x: float = Field(gt=0)
    scale_y: float = Field(gt=0)
