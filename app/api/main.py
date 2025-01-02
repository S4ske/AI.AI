from fastapi import APIRouter
from app.api.routers import users, auth, projects

api_router = APIRouter()
api_router.include_router(users.router, tags=["users"])
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(projects.router, tags=["projects"])
