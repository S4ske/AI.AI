from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(str(settings.POSTGRES_URL_ASYNC))
