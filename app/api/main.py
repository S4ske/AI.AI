from fastapi import APIRouter
from app.api.routers import users, auth, video

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(video.router, tags=["render_without_auth"])
