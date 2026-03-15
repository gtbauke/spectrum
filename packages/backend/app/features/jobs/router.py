import logging

from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query

from app.features.profiles.guards.get_latest_profile_version_id import get_latest_profile_version_id
from core.models.jobs.where import JobFilter, JobVersionFilter, JobWhere
from core.ports.unit_of_work import UnitOfWork
from core.utils.filters.field_filter import StringFilter

from app.api.response import PaginatedResponse
from app.api.unit_of_work import get_uow
from app.features.datasets.router import get_current_owner
from app.features.profiles.guards.can_edit_profile import can_edit_profile

from .service import JobsService, get_jobs_service
from .dto.create_job import CreateJob, CreateJobBody
from .dto.update_job import UpdateJob, UpdateJobBody

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
    data: CreateJobBody,
    uow: UnitOfWork = Depends(get_uow),
    jobs_service: JobsService = Depends(get_jobs_service),
    owner_id: UUID = Depends(get_current_owner),
    profile_version_id: UUID = Depends(get_latest_profile_version_id),
):
    return await jobs_service.create(
        uow=uow,
        data=CreateJob(
            owner_id=owner_id,
            profile_version_id=profile_version_id,
            version=data.version,
        )
    )


@jobs_router.get(
    path="/",
)
async def get_jobs(
    uow: UnitOfWork = Depends(get_uow),
    jobs_service: JobsService = Depends(get_jobs_service),
    size: int = Query(20, ge=1, le=100),
    page: int = Query(1, ge=1),
    name: Optional[str] = Query(None),
):
    version = JobVersionFilter(
        name=StringFilter(ilike=f"%{name}%") if name else None,
    ) if name else None

    filter = JobFilter(
        versions=version,
    )

    offset = (page - 1) * size
    items, total = await jobs_service.get_paginated(uow=uow, filter=filter, limit=size, offset=offset)

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@jobs_router.post(
    path="/{job_id}",
    dependencies=[
        Depends(can_edit_profile),
    ]
)
async def create_new_version(
    profile_id: UUID,
    job_id: UUID,
    data: UpdateJobBody,
    uow: UnitOfWork = Depends(get_uow),
    jobs_service: JobsService = Depends(get_jobs_service),
    owner_id: UUID = Depends(get_current_owner),
    profile_version_id: UUID = Depends(get_latest_profile_version_id),
):
    return await jobs_service.create_new_version(
        uow=uow,
        data=UpdateJob(
            new_owner_id=data.new_owner_id,
            owner_id=owner_id,
            profile_version_id=profile_version_id,
            version=data.version,
        ),
        where=JobWhere(
            id=job_id,
        )
    )
