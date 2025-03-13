import os
from typing import TypeVar

from celery import Celery
from PIL import Image
from pydantic import BaseModel
from redis import Redis

from app.core.config import settings
from app.rendering.render import render_video
from app.rendering.schemas import AnimatedImageParams
from app.schemas import AnimatedImageSchema, AnimationSchema
from app.utils import create_linear_animated_image

redis_client = Redis(
    host=settings.REDIS_HOST,
    port=6379,
    decode_responses=True,
    password=settings.REDIS_PASSWORD,
)

celery_app = Celery()
celery_app.conf.broker_url = settings.REDIS_URL
celery_app.conf.result_backend = settings.REDIS_URL


Schema = TypeVar("Schema", bound=BaseModel)
Model = TypeVar("Model")


@celery_app.task(name="render_with_redis", ignore_result=True)
def render_with_redis(
    project_name: str,
    images_paths: list[str],
    shape: tuple[int, int],
    fps: int,
    duration: int,
    background_color: tuple[float, float, float],
    animated_images_names: list[str],
    animated_images_living_starts: list[float],
    animated_images_living_ends: list[float],
    animated_images_params: list[dict],
    animated_images_animations: list[list[dict]],
):
    redis_client.set(project_name, "in progress")
    try:
        images_dict = {}
        for image_path in images_paths:
            file = Image.open(image_path)
            images_dict[os.path.split(file.filename)[-1]] = file
        animated_images = []
        for i in range(len(animated_images_names)):
            params = AnimatedImageParams(
                x=float(animated_images_params[i]["x"]),
                y=float(animated_images_params[i]["y"]),
                angle=float(animated_images_params[i]["angle"]),
                opacity=float(animated_images_params[i]["opacity"]),
                scale_x=float(animated_images_params[i]["scale_x"]),
                scale_y=float(animated_images_params[i]["scale_y"]),
            )
            animations = []
            for j in range(len(animated_images_animations[i])):
                animations.append(
                    AnimationSchema(
                        param_name=str(animated_images_animations[i][j]["param_name"]).split(".")[-1],
                        start_time=float(animated_images_animations[i][j]["start_time"]),
                        end_time=float(animated_images_animations[i][j]["end_time"]),
                        start_point=float(animated_images_animations[i][j]["start_point"]),
                        end_point=float(animated_images_animations[i][j]["end_point"]),
                    )
                )
            animated_image_schema = AnimatedImageSchema(
                name=str(animated_images_names[i]),
                living_start=float(animated_images_living_starts[i]),
                living_end=float(animated_images_living_ends[i]),
                params=params,
                animations=animations,
            )
            animated_images.append(
                create_linear_animated_image(images_dict[animated_images_names[i]], animated_image_schema)
            )
        render_video(
            os.path.join(settings.VIDEOS_PATH, project_name + ".mp4"),
            animated_images,
            shape,
            fps,
            duration,
            "mp4v",
            (background_color[0], background_color[1], background_color[2], 255),
        )
        delete_file.apply_async(
            (os.path.join(settings.VIDEOS_PATH, project_name + ".mp4"),),
            countdown=settings.VIDEOS_TTL,
        )
        redis_client.set(project_name, "completed", ex=settings.VIDEOS_TTL)
    except Exception as e:
        redis_client.set(project_name, "failed")
        raise e


@celery_app.task(name="delete_file", ignore_result=True)
def delete_file(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)
