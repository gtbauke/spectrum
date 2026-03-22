from fastapi import APIRouter
from app.features.users.router import users_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(users_router, prefix="/users", tags=["Users"])
