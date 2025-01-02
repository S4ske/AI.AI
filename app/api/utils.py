from redis.asyncio import Redis
from app.rendering.classes import AnimatedImage
from app.rendering.render import render_video
import os
from app.core.config import settings

redis_client = Redis(host=settings.REDIS_HOST, port=6379, decode_responses=True)


async def render_with_redis(
    user_id: str,
    video_name: str,
    animated_images: list[AnimatedImage],
    shape: tuple[int, int],
    fps: int,
    duration: float,
):
    await redis_client.set(video_name, "in progress")
    try:
        render_video(
            os.path.join(settings.VIDEOS_PATH, user_id, video_name + ".mp4"),
            animated_images,
            shape,
            fps,
            duration,
            "mp4v",
        )
        await redis_client.set(video_name, "completed", ex=settings.VIDEOS_TTL)
    except Exception as e:
        await redis_client.set(video_name, "failed")
        raise e
