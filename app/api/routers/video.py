import os.path
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
from app.schemas import ProjectSchema
from PIL import Image
from pydantic import ValidationError, BaseModel
from fastapi.encoders import jsonable_encoder
from io import BytesIO
from app.api.utils import render_with_redis, redis_client
from app.core.config import settings
from app.utils import create_linear_animated_image

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
    bg_tasks: BackgroundTasks,
    files: list[UploadFile] = File(default=[]),
    render_info: ProjectSchema = Depends(Checker(ProjectSchema)),
) -> bool:
    anim_images = []
    images_dict = {}
    for file in files:
        images_dict[file.filename] = Image.open(BytesIO(await file.read()))
    for source in render_info.animated_images:
        file = images_dict.get(source.name)
        if not file:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        anim_images.append(
            create_linear_animated_image(file, source)
        )
    background_color = render_info.background_color
    bg_tasks.add_task(
        render_with_redis,
        render_info.name,
        anim_images,
        render_info.shape,
        render_info.fps,
        render_info.duration,
        (background_color[0], background_color[1], background_color[2], 255)
    )
    return True


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
    render_status = await redis_client.get(video_name)
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
        render_status = await redis_client.get(video_name)
        if not render_status or render_status != "completed":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return FileResponse(
            path=os.path.join(settings.VIDEOS_PATH, video_name + ".mp4"),
            filename=video_name + ".mp4",
            media_type="video/mp4",
        )
    except RuntimeError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
