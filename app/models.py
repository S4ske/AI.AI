from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime
from uuid import uuid4, UUID

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    email = mapped_column(String(255), unique=True, index=True)
    username = mapped_column(String(length=255), default=None, nullable=True)
    hashed_password = mapped_column(String)
    is_active = mapped_column(Boolean, default=False)
    is_superuser = mapped_column(Boolean, default=False)
    created_at = mapped_column(DateTime)
    updated_at = mapped_column(DateTime)
