from fastapi import APIRouter
from app.features.users.router import users_router
from app.features.auth.router import auth_router
from app.features.datasets.routers.datasets import datasets_router
from app.features.profiles.routers.profiles import profiles_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(datasets_router, prefix="/datasets", tags=["Datasets"])
api_router.include_router(profiles_router, prefix="/profiles", tags=["Profiles"])
