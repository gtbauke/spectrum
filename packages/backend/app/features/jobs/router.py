import logging

from uuid import UUID
from fastapi import APIRouter, Depends

from core.ports.unit_of_work import UnitOfWork

from app.api.unit_of_work import get_uow
from app.features.profiles.guards.can_edit_profile import can_edit_profile

from .service import JobsService, get_jobs_service
from .dto.create_job import CreateJob

logger = logging.getLogger(__name__)
jobs_router = APIRouter(tags=["jobs"])


@jobs_router.post(
    path="/",
    dependencies=[
        Depends(can_edit_profile)
    ]
)
async def create_job(
    profile_id: UUID,
    data: CreateJob,
    uow: UnitOfWork = Depends(get_uow),
    jobs_service: JobsService = Depends(get_jobs_service),
):
    return await jobs_service.create(
        uow=uow,
        data=data.model_copy(
            update={
                "profile_id": profile_id,
            }
        ),
    )
