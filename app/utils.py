from app.schemas import AnimationSchema, AnimatedImageSchema
from app.rendering.classes import AnimatedImage, Animation, LinearInterpolator
from PIL import Image


def create_linear_animation(animation_schema: AnimationSchema) -> Animation:
    return Animation(
        animation_schema.param_name,
        animation_schema.start_time,
        animation_schema.end_time,
        animation_schema.start_point,
        animation_schema.end_point,
        LinearInterpolator(),
    )


def create_linear_animated_image(
    image: Image, animated_image_schema: AnimatedImageSchema
) -> AnimatedImage:
    return AnimatedImage(
        image,
        animated_image_schema.name,
        animated_image_schema.living_start,
        animated_image_schema.living_end,
        animated_image_schema.params,
        list(map(create_linear_animation, animated_image_schema.animations)),
    )
