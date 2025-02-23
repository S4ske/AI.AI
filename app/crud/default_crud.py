from typing import Type, TypeVar
from app.models import Base
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

T = TypeVar("T", bound=Base)


async def create_model(
    db_session: AsyncSession, schema: BaseModel, model_type: Type[T]
) -> T:
    schema_dict = schema.model_dump()
    model = model_type(**schema_dict)
    db_session.add(model)
    await db_session.commit()
    await db_session.refresh(model)
    return model
