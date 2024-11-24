import cv2
from PIL import Image
import numpy as np
from app.classes import AnimatedImage
from app.schemas import AnimatedImageParams


def apply_params(image: Image.Image, params: AnimatedImageParams) -> Image.Image:
    result = image

    result = result.rotate(params.angle)
    result.putalpha(int(params.opacity))
    result = result.resize((int(params.scale_x), int(params.scale_y)))

    return result


def render_video(
    name: str,
    animated_images: list[AnimatedImage],
    shape: tuple[int, int],
    fps: int,
    duration: float,
):
    background = Image.new("RGBA", size=shape, color=(190, 190, 190, 255))
    video = cv2.VideoWriter(name, cv2.VideoWriter.fourcc(*"mp4v"), fps, shape)
    total_frames = int(fps * duration)

    for frame_i in range(total_frames):
        time = duration * (frame_i / total_frames)
        curr_frame = background.copy()

        for anim_img in animated_images:
            img_params = anim_img.interpolate(time)
            if not img_params:
                continue
            processed = apply_params(anim_img.image, img_params)
            curr_frame.paste(
                processed, (int(img_params.x), int(img_params.y)), processed
            )

        cv_frame = cv2.cvtColor(np.array(curr_frame), cv2.COLOR_RGBA2BGR)
        video.write(cv_frame)

    video.release()
