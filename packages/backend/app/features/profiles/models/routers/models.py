from uuid import UUID
from fastapi import APIRouter, Depends, status

from app.api.unit_of_work import get_uow
from app.features.profiles.models.errors.model_not_found import ModelNotFound
from core.ports.unit_of_work import UnitOfWork

from app.features.auth.guards.get_current_user import get_current_user

from core.features.profiles.models.model import Model
from core.features.profiles.models.where import ModelWhere, ModelFilter
from core.utils.filters.field_filter import UUIDFilter
from core.utils.pagination.response import PaginatedResponse
from core.utils.pagination.base import Pagination

from app.features.profiles.models.responses.model_name import ModelNameResponse

models_router = APIRouter()


@models_router.get(
    path="/names",
    response_model=list[ModelNameResponse],
    dependencies=[Depends(dependency=get_current_user)],
)
async def list_model_names(
    profile_id: UUID,
    uow: UnitOfWork = Depends(dependency=get_uow),
):
    model_filter = ModelFilter(profile_id=UUIDFilter(eq=profile_id))
    
    models = await uow.models.list_all(
        filter=model_filter,
    )
    
    return [ModelNameResponse(name=model.name) for model in models]


@models_router.get(
    path="",
    response_model=PaginatedResponse[Model],
    dependencies=[Depends(dependency=get_current_user)],
)
async def list_models(
    profile_id: UUID,
    pagination: Pagination = Depends(),
    uow: UnitOfWork = Depends(dependency=get_uow),
):
    model_filter = ModelFilter(profile_id=UUIDFilter(eq=profile_id))
    
    models = await uow.models.list(
        filter=model_filter,
        pagination=pagination,
    )
    
    return models


@models_router.get(
    path="/{model_id}",
    response_model=Model,
    dependencies=[Depends(dependency=get_current_user)],
)
async def get_model(
    profile_id: UUID,
    model_id: UUID,
    uow: UnitOfWork = Depends(dependency=get_uow),
):
    where = ModelWhere(id=model_id)
    model = await uow.models.get_unique(where=where)

    if not model or model.profile_id != profile_id:
        raise ModelNotFound()

    return model
