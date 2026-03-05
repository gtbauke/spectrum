from fastapi import APIRouter


from app.features.users.router import users_router
from app.features.auth.router import auth_router

api_router = APIRouter(prefix="/v1")

api_router.include_router(prefix="/users", router=users_router)
api_router.include_router(prefix="/auth", router=auth_router)
