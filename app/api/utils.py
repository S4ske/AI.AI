from redis import Redis
from app.classes import AnimatedImage
from app.rendering.render import render_video
from app.core.config import settings

redis_client = Redis(host=settings.REDIS_HOST, port=6379, decode_responses=True)


def render_with_redis(
    name: str,
    animated_images: list[AnimatedImage],
    shape: tuple[int, int],
    fps: int,
    duration: float,
):
    redis_client.hset(name, "status", "in progress")
    try:
        render_video(name, animated_images, shape, fps, duration)
        redis_client.hset(name, "status", "completed")
    except Exception as e:
        redis_client.hset(name, "status", "failed")
        raise e
