from redis.asyncio import Redis
from app.rendering.classes import AnimatedImage
from app.rendering.render import render_video
import os
from app.core.config import settings
from celery import Celery

redis_client = Redis(host=settings.REDIS_HOST, port=6379, decode_responses=True)

celery_app = Celery()
celery_app.conf.broker_url = settings.REDIS_URL
celery_app.conf.result_backend = settings.REDIS_URL


async def render_with_redis(
    video_name: str,
    animated_images: list[AnimatedImage],
    shape: tuple[int, int],
    fps: int,
    duration: float,
    background_color: tuple[int, ...]
):
    await redis_client.set(video_name, "in progress")
    try:
        await render_video(
            os.path.join(settings.VIDEOS_PATH, video_name + ".mp4"),
            animated_images,
            shape,
            fps,
            duration,
            "mp4v",
            background_color,
        )
        delete_video_file.apply_async(
            (os.path.join(settings.VIDEOS_PATH, video_name + ".mp4"),),
            countdown=settings.VIDEOS_TTL,
        )
        await redis_client.set(video_name, "completed", ex=settings.VIDEOS_TTL)
    except Exception as e:
        await redis_client.set(video_name, "failed")
        raise e


@celery_app.task(name="delete_video_file", ignore_result=True)
def delete_video_file(video_path: str) -> None:
    if os.path.exists(video_path):
        os.remove(video_path)
