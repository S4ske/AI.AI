import os

from dotenv import load_dotenv
from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    VIDEOS_TTL: int

    PROJECT_PATH: str
    VIDEOS_PATH: str

    PHOTOS_PATH: str

    @computed_field
    @property
    def FULL_VIDEOS_PATH(self) -> str:  # noqa: N802
        return os.path.join(self.PROJECT_PATH, self.VIDEOS_PATH)

    @computed_field
    @property
    def REDIS_URL(self) -> str:  # noqa: N802
        return "redis://" + self.REDIS_HOST + ":" + str(self.REDIS_PORT)

    @computed_field
    @property
    def POSTGRES_URL(self) -> PostgresDsn:  # noqa: N802
        return MultiHostUrl.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @computed_field
    @property
    def POSTGRES_URL_ASYNC(self) -> PostgresDsn:  # noqa: N802
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()
