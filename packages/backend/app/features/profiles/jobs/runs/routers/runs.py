import asyncio

from uuid import UUID
from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse

from app.api.unit_of_work import get_uow
from core.ports.unit_of_work import UnitOfWork

from app.features.auth.guards.get_current_user import get_current_user
from app.features.profiles.jobs.guards.can_edit_job import can_edit_job
from app.features.profiles.jobs.runs.errors.run_not_found import RunNotFound

from core.features.profiles.jobs.runs.run import Run
from core.features.profiles.jobs.runs.events import RunCreatedEvent
from core.features.profiles.jobs.runs.where import RunWhere, RunFilter
from core.features.profiles.jobs.runs.status import JobRunStatus
from core.utils.filters.field_filter import UUIDFilter
from core.utils.pagination.response import PaginatedResponse
from core.utils.pagination.base import Pagination

runs_router = APIRouter()


@runs_router.post(
    path="",
    response_model=Run,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(dependency=can_edit_job)],
)
async def create_run(
    job_id: UUID,
    uow: UnitOfWork = Depends(dependency=get_uow),
):
    latest_run = await uow.runs.get_latest_version(parent_id=job_id)

    version = 1
    id = None

    if latest_run:
        version = latest_run.version + 1
        id = latest_run.id

    run = Run.new(id=id, job_id=job_id, version=version)

    await uow.runs.unset_latest_and_add(parent_id=job_id, new_entity=run)

    event = RunCreatedEvent(
        run_id=run.id, job_id=run.job_id, version=run.version)
    uow.events_publisher.publish(
        routing_key=event.routing_key,
        payload=event.model_dump(mode="json"),
    )

    return run


@runs_router.get(
    path="",
    response_model=PaginatedResponse[Run],
    dependencies=[Depends(dependency=get_current_user)],
)
async def list_runs(
    job_id: UUID,
    pagination: Pagination = Depends(),
    uow: UnitOfWork = Depends(dependency=get_uow),
):
    run_filter = RunFilter(job_id=UUIDFilter(eq=job_id))

    runs = await uow.runs.list(
        filter=run_filter,
        pagination=pagination,
    )

    return runs


@runs_router.get(
    path="/{run_id}",
    response_model=Run,
    dependencies=[Depends(dependency=get_current_user)],
)
async def get_run(
    job_id: UUID,
    run_id: UUID,
    uow: UnitOfWork = Depends(dependency=get_uow),
):
    where = RunWhere(id=run_id, is_latest=True)
    run = await uow.runs.get_unique(where=where)

    if not run or run.job_id != job_id:
        raise RunNotFound()

    return run


@runs_router.get(
    path="/{run_id}/stream",
    dependencies=[Depends(dependency=get_current_user)],
)
async def get_run_stream(
    job_id: UUID,
    run_id: UUID,
    uow: UnitOfWork = Depends(dependency=get_uow),
):
    where = RunWhere(id=run_id, is_latest=True)

    async def event_generator():
        last_status = None
        seconds_since_last_emit = 0

        while True:
            run = await uow.runs.get_unique(where=where)

            if not run or run.job_id != job_id:
                raise RunNotFound()

            if run.status != last_status:
                yield f"data: {run.model_dump_json()}\n\n"
                last_status = run.status
                seconds_since_last_emit = 0
            else:
                seconds_since_last_emit += 1
                if seconds_since_last_emit >= 15:
                    yield ": ping\n\n"
                    seconds_since_last_emit = 0

            if run.status == JobRunStatus.FINISHED or run.status == JobRunStatus.FAILED:
                break

            await asyncio.sleep(1)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
