from fastapi import (
    APIRouter,
    UploadFile,
    HTTPException,
    status,
    Depends,
    File,
    Form,
    BackgroundTasks,
)
from fastapi.responses import FileResponse, JSONResponse
from app.schemas import RenderRequest
from app.classes import AnimatedImage
from PIL import Image
from pydantic import ValidationError, BaseModel
from fastapi.encoders import jsonable_encoder
from io import BytesIO
from app.api.utils import render_with_redis, redis_client

router = APIRouter()


class Checker:
    def __init__(self, model: type[BaseModel]) -> None:
        self.model = model

    def __call__(self, data: str = Form()):
        try:
            return self.model.model_validate_json(data)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=jsonable_encoder(e.errors()),
            )


@router.post("/render_wa")
async def render(
    bg_tasks: BackgroundTasks,
    files: list[UploadFile] = File(),
    render_info: RenderRequest = Depends(Checker(RenderRequest)),
) -> bool:
    anim_images = []
    for source in render_info.animated_images:
        curr_files: list[UploadFile] = list(
            filter(lambda x: x.filename == source.name, files)
        )
        if not curr_files:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        file = curr_files[0]
        anim_images.append(
            AnimatedImage.create_from_source(
                Image.open(BytesIO(await file.read())), source
            )
        )
    bg_tasks.add_task(
        render_with_redis,
        render_info.name,
        anim_images,
        render_info.shape,
        render_info.fps,
        render_info.duration,
    )
    return True


@router.get("/check_video/{name}")
async def check_video(video_name: str) -> JSONResponse:
    render_dict = redis_client.hgetall(video_name)
    if not render_dict or not render_dict.get("status"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(render_dict)


@router.get("/video_wa")
async def get_video(video_name: str) -> FileResponse:
    try:
        render_dict = redis_client.hgetall(video_name)
        if not render_dict or not render_dict.get("status") == "completed":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return FileResponse(
            path=video_name, filename=video_name, media_type="video/mp4"
        )
    except RuntimeError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
