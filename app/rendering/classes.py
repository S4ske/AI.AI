from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any

from PIL import Image

from app.rendering.schemas import (
    AnimatedImageParams,
    AnimationParam,
)


class Interpolator(ABC):
    def interpolate(self, time: float, animation: "Animation") -> float | int:
        if time >= animation.end_time:
            return animation.end_point
        elif time <= animation.start_time:
            return animation.start_point
        return self._calculate_params(time, animation)

    @abstractmethod
    def _calculate_params(self, time: float, animation: "Animation") -> float | int:
        pass


class LinearInterpolator(Interpolator):
    def _calculate_params(self, time: float, animation: "Animation") -> float | int:
        return animation.start_point + (
            (time - animation.start_time) / (animation.end_time - animation.start_time)
        ) * (animation.end_point - animation.start_point)


class Animation:
    def __init__(
        self,
        param_name: AnimationParam,
        start_time: float,
        end_time: float,
        start_point: Any,
        end_point: Any,
        interpolator: Interpolator,
    ) -> None:
        self.param_name = param_name
        self.start_time = start_time
        self.end_time = end_time
        self.start_point = start_point
        self.end_point = end_point
        self.interpolator = interpolator

    def interpolate(self, time: float) -> Any:
        return self.interpolator.interpolate(time, self)


class AnimatedImage:
    def __init__(
        self,
        image: Image.Image,
        name: str,
        living_start: float,
        living_end: float,
        params: AnimatedImageParams,
        animations: list[Animation],
    ) -> None:
        self.image = image
        self.name = name
        self.living_start = living_start
        self.living_end = living_end
        self.last_params = params
        self.animations = []
        self.animations = deepcopy(animations)
        self.animations.sort(key=lambda x: x.start_time)

    def interpolate(self, time: float) -> AnimatedImageParams | None:
        if time < self.living_start or time > self.living_end:
            return None
        res = self.last_params.model_dump()
        for animation in filter(lambda x: x.start_time <= time, self.animations):
            new_value = animation.interpolate(time)
            if new_value is not None:
                res[animation.param_name.value] = new_value
        self.last_params = AnimatedImageParams(**res)
        return self.last_params
