from PIL import Image
from typing import Any
from app.schemas import (
    AnimationParam,
    AnimatedImageParams,
    AnimatedImageSchema,
    AnimationSchema,
)


def linear_interpolate(time: float, animation: "Animation") -> Any:
    if time >= animation.end_time:
        return animation.end_point
    elif time <= animation.start_time:
        return animation.start_point
    return animation.start_point + (
        (time - animation.start_time) / (animation.end_time - animation.start_time)
    ) * (animation.end_point - animation.start_point)


class Animation:
    interpolation_functions = {
        AnimationParam.x: linear_interpolate,
        AnimationParam.y: linear_interpolate,
        AnimationParam.opacity: linear_interpolate,
        AnimationParam.angle: linear_interpolate,
        AnimationParam.scale_x: linear_interpolate,
        AnimationParam.scale_y: linear_interpolate,
    }

    def __init__(
        self,
        param_name: AnimationParam,
        start_time: float,
        end_time: float,
        start_point: Any,
        end_point: Any,
    ) -> None:
        self.param_name = param_name
        self.start_time = start_time
        self.end_time = end_time
        self.start_point = start_point
        self.end_point = end_point

    def interpolate(self, time: float) -> Any:
        return self.interpolation_functions[self.param_name](time, self)

    @classmethod
    def create_from_schema(cls, animation_schema: AnimationSchema) -> "Animation":
        return Animation(
            animation_schema.param_name,
            animation_schema.start_time,
            animation_schema.end_time,
            animation_schema.start_point,
            animation_schema.end_point,
        )


class AnimatedImage:
    def __init__(
        self,
        image: Image.Image,
        name: str,
        living_start: float,
        living_end: float,
        params: AnimatedImageParams,
        animations: list[AnimationSchema],
    ) -> None:
        self.image = image
        self.name = name
        self.living_start = living_start
        self.living_end = living_end
        self.last_params = params
        self.animations = []
        for animation in animations:
            self.animations.append(Animation.create_from_schema(animation))
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

    @classmethod
    def create_from_source(
        cls, image: Image.Image, source: AnimatedImageSchema
    ) -> "AnimatedImage":
        return AnimatedImage(
            image,
            source.name,
            source.living_start,
            source.living_end,
            source.params,
            source.animations,
        )
