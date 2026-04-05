from uuid import UUID
from fastapi import APIRouter, Depends, status, Query
from typing import cast

from app.api.unit_of_work import get_uow
from app.features.profiles.blocks.errors.block_not_found import BlockNotFound
from app.features.profiles.blocks.inference.errors.inference_run_not_found import InferenceRunNotFound
from app.features.profiles.guards.can_edit_profile import can_edit_profile
from core.ports.unit_of_work import UnitOfWork
from core.features.profiles.blocks.block_kind import BlockKind, InferenceBlock
from core.features.profiles.blocks.inference.inference_run import InferenceRun
from core.features.profiles.blocks.inference.events import InferenceRunRequestedEvent
from core.features.profiles.blocks.inference.where import InferenceRunFilter, InferenceRunWhere
from core.features.profiles.blocks.where import BlockWhere
from core.utils.filters.field_filter import UUIDFilter
from core.utils.pagination.base import Pagination
from core.utils.pagination.response import PaginatedResponse

inference_router = APIRouter()


@inference_router.get(
    path="/{block_id}/runs",
    response_model=PaginatedResponse[InferenceRun],
    dependencies=[Depends(can_edit_profile)]
)
async def get_inference_runs(
    block_id: UUID,
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    uow: UnitOfWork = Depends(get_uow)
):
    runs_filter = InferenceRunFilter(
        block_id=UUIDFilter(eq=block_id),
    )

    pagination = Pagination(offset=offset, limit=limit)
    response = await uow.inference_runs.list(runs_filter, pagination)

    return response


@inference_router.get(
    path="/{block_id}/runs/{run_id}",
    response_model=InferenceRun,
    dependencies=[Depends(can_edit_profile)]
)
async def get_inference_run(
    block_id: UUID,
    run_id: UUID,
    uow: UnitOfWork = Depends(get_uow)
):
    run = await uow.inference_runs.get_unique(InferenceRunWhere(id=run_id))

    if not run or run.block_id != block_id:
        raise InferenceRunNotFound()

    return run


@inference_router.post(
    path="/{block_id}/runs",
    response_model=InferenceRun,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(can_edit_profile)]
)
async def create_inference_run(
    profile_id: UUID,
    block_id: UUID,
    uow: UnitOfWork = Depends(get_uow)
):
    block = await uow.blocks.get_unique(BlockWhere(id=block_id))
    if not block or block.profile_id != profile_id:
        raise BlockNotFound()

    if block.kind != BlockKind.INFERENCE:
        raise BlockNotFound()

    inference_data = cast(InferenceBlock, block.data)

    latest = await uow.inference_runs.get_latest_version(parent_id=block_id)
    next_version = (latest.version + 1) if latest else 1

    run = InferenceRun.new(
        block_id=block_id,
        profile_id=profile_id,
        query=inference_data.data,
        version=next_version,
    )

    await uow.inference_runs.unset_latest_and_add(parent_id=block_id, new_entity=run)

    event = InferenceRunRequestedEvent(
        run_id=run.id,
        block_id=block_id,
        profile_id=profile_id,
        query=run.query
    )

    uow.events_publisher.publish(
        routing_key=event.routing_key,
        payload=event.model_dump(mode="json"),
    )

    return run
