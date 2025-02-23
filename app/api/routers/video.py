import os
from fastapi import (
    APIRouter,
    UploadFile,
    HTTPException,
    status,
    Depends,
    File,
    Form,
)
from fastapi.responses import FileResponse, JSONResponse
from app.schemas import ProjectSchema
from pydantic import ValidationError, BaseModel
from fastapi.encoders import jsonable_encoder
from app.api.utils import render_with_redis, redis_client, delete_file
from app.core.config import settings
from random import randint
from PIL import Image
from io import BytesIO
from app.schemas import AnimationSchema
from typing import Any

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


@router.post(
    "/render_wa",
    description="Эндпоинт для начала рендера. В files передаются изображения учавствующие "
    "в анимации. В data передаются json СТРОКА (не реальный application/json, а "
    "именно строка в формате json, т.к. весь запрос в формате multiaprt/form-data) "
    "соответсвующая схеме RenderRequest (указан ниже в блоке Schemas). В поле "
    "'animated_images' схемы RenderRequest анимированные изображения имеют имена "
    "соответсвующих им файлам из files и расположены в порядке расположения на "
    "холсте, от тех, которые дальше от нас (на заднем фоне) к тем, которые ближе. "
    "Если не выдаёт ошибку, то всегда возвращает True. Видео удаляется через 10 "
    "минут, после того как отрендерилось.",
    response_model=bool,
)
async def render(
    files: list[UploadFile] = File(default=[]),
    project_schema: ProjectSchema = Depends(Checker(ProjectSchema)),
) -> bool:
    directory_name = str(randint(0, 100000))
    directory_path = os.path.join(settings.PHOTOS_PATH, directory_name)
    os.makedirs(directory_path, exist_ok=True)
    images_paths = []
    for file in files:
        filename = file.filename
        image_path = os.path.join(directory_path, filename)
        image = Image.open(BytesIO(await file.read()))
        image.save(image_path)
        delete_file.apply_async(
            (image_path,),
            countdown=settings.VIDEOS_TTL + 60,
        )
        images_paths.append(image_path)
    render_with_redis.apply_async(
        (
            project_schema.name,
            images_paths,
            project_schema.shape,
            project_schema.fps,
            project_schema.duration,
            project_schema.background_color,
            list(map(lambda x: x.name, project_schema.animated_images)),
            list(map(lambda x: x.living_start, project_schema.animated_images)),
            list(map(lambda x: x.living_end, project_schema.animated_images)),
            list(map(lambda x: x.params.model_dump(), project_schema.animated_images)),
            list(
                map(
                    lambda x: list(map(model_dump_animation, x.animations)),
                    project_schema.animated_images,
                )
            ),
        )
    )
    return True


def model_dump_animation(animation: AnimationSchema) -> dict[str, Any]:
    dump = animation.model_dump()
    dump["param_name"] = str(dump["param_name"])
    return dump


@router.get(
    "/check_video/{video_name}",
    description="Эндпоинт для проверки состояния рендера видео. Возвращает json "
    "со статусом рендера. Всего есть три состояния: "
    "'in progress', 'completed', 'failed'. Думаю, говорят сами за себя. "
    "Если видео с таким именем не существует или оно уже удалено, "
    "то возвращает ошибку 404_NOT_FOUND.",
    response_class=JSONResponse,
)
async def check_video(video_name: str) -> JSONResponse:
    render_status = redis_client.get(video_name)
    if not render_status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(render_status)


@router.get(
    "/video_wa/{video_name}",
    description="Если видео с таким именем существует и его статус равен 'completed', "
    "то возвращает это видео в формате video/mp4. Названо оно <video_name>.mp4. "
    "Иначе ошибка 404_NOT_FOUND",
    response_class=FileResponse,
)
async def get_video(video_name: str) -> FileResponse:
    try:
        render_status = redis_client.get(video_name)
        if not render_status or render_status != "completed":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return FileResponse(
            path=os.path.join(settings.VIDEOS_PATH, video_name + ".mp4"),
            filename=video_name + ".mp4",
            media_type="video/mp4",
        )
    except RuntimeError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
