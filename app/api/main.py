from fastapi import APIRouter

from app.api.routers import auth, projects, users, video_wa

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(video_wa.router, tags=["render_without_auth"])
api_router.include_router(projects.router, tags=["projects"])
