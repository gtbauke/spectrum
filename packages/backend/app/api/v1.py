from fastapi import APIRouter


from app.features.users.router import users_router
from app.features.auth.router import auth_router
from app.features.owners.router import owners_router
from app.features.datasets.router import datasets_router

api_router = APIRouter(prefix="/v1")

api_router.include_router(prefix="/users", router=users_router)
api_router.include_router(prefix="/auth", router=auth_router)
api_router.include_router(prefix="/owners", router=owners_router)
api_router.include_router(prefix="/datasets", router=datasets_router)
