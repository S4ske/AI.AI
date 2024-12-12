import cv2
from PIL import Image
import numpy as np
from app.rendering.classes import AnimatedImage
from app.schemas import AnimatedImageParams


def apply_params(image: Image.Image, params: AnimatedImageParams) -> Image.Image:
    result = image.convert("RGBA")

    r, g, b, a = result.split()
    alpha_data = a.load()
    for x in range(result.width):
        for y in range(result.height):
            if alpha_data[x, y] != 0:
                alpha_data[x, y] = int(params.opacity)
    result = Image.merge("RGBA", (r, g, b, a))
    result = result.resize((int(params.scale_x), int(params.scale_y)))
    result = result.rotate(params.angle)

    return result


def render_video(
    video_path: str,
    animated_images: list[AnimatedImage],
    shape: tuple[int, int],
    fps: int,
    duration: float,
    codec: str,
    background_color: tuple[float, ...] = (190, 190, 190, 255),
):
    background = Image.new("RGBA", size=shape, color=background_color)
    video = cv2.VideoWriter(video_path, cv2.VideoWriter.fourcc(*codec), fps, shape)
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
