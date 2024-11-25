ARG PYTHON_VERSION=3.11.9
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

ENV POETRY_VIRTUALENVS_CREATE=false

ENV PYTHONPATH=/app

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && apt-get clean

RUN pip install poetry --no-cache-dir

RUN poetry install --only main --no-interaction

EXPOSE 8000

CMD alembic checkout head && uvicorn 'app.main:app' --host=0.0.0.0 --port=8000