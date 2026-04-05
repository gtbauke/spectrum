from uuid import UUID
from fastapi import APIRouter, Depends, status, Query

from app.api.unit_of_work import get_uow
from app.features.profiles.blocks.errors.block_not_found import BlockNotFound
from app.features.profiles.blocks.inference.routers.inference import inference_router
from core.ports.unit_of_work import UnitOfWork

from app.features.auth.guards.get_current_user import get_current_user
from app.features.profiles.guards.can_edit_profile import can_edit_profile

from app.features.profiles.blocks.dtos.create import CreateBlockDto
from app.features.profiles.blocks.dtos.update import UpdateBlockDto, BulkUpdateBlockDto

from core.features.profiles.blocks.block import Block
from core.features.profiles.blocks.where import BlockWhere, BlockFilter
from core.utils.filters.field_filter import UUIDFilter

blocks_router = APIRouter()

blocks_router.include_router(inference_router)


@blocks_router.post("", response_model=list[Block], status_code=status.HTTP_201_CREATED, dependencies=[Depends(can_edit_profile)])
async def create_blocks(
    profile_id: UUID,
    dtos: list[CreateBlockDto],
    uow: UnitOfWork = Depends(get_uow)
):
    blocks = [
        Block.new(
            profile_id=profile_id,
            kind=dto.data.kind,
            order_index=dto.order_index,
            data=dto.data
        ) for dto in dtos
    ]

    await uow.blocks.add_many(blocks)
    return blocks


@blocks_router.put("", response_model=list[Block], dependencies=[Depends(can_edit_profile)])
async def bulk_update_blocks(
    profile_id: UUID,
    dtos: list[BulkUpdateBlockDto],
    uow: UnitOfWork = Depends(get_uow)
):
    blocks = []
    for dto in dtos:
        block = await uow.blocks.get_unique(BlockWhere(id=dto.id))

        if not block or block.profile_id != profile_id:
            raise BlockNotFound()

        updated_block = block.model_copy(
            update=dto.model_dump(exclude_unset=True),
        )

        blocks.append(updated_block)

    await uow.blocks.update_many(blocks)
    return blocks


@blocks_router.put("/{block_id}", response_model=Block, dependencies=[Depends(can_edit_profile)])
async def update_block(
    profile_id: UUID,
    block_id: UUID,
    dto: UpdateBlockDto,
    uow: UnitOfWork = Depends(get_uow)
):
    block = await uow.blocks.get_unique(BlockWhere(id=block_id))

    if not block or block.profile_id != profile_id:
        raise BlockNotFound()

    if dto.data is not None and dto.data.kind != block.kind:
        raise BlockNotFound()

    update_data = dto.model_dump(exclude_unset=True)
    domain_block = Block(
        id=block.id,
        profile_id=profile_id,
        kind=block.kind,
        order_index=update_data.get("order_index", block.order_index),
        data=update_data.get("data", block.data)
    )

    updated_block = block.model_copy(
        update=domain_block.model_dump(exclude_unset=True)
    )

    await uow.blocks.update(updated_block)
    return updated_block


@blocks_router.delete("", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(can_edit_profile)])
async def bulk_delete_blocks(
    profile_id: UUID,
    block_ids: list[UUID],
    uow: UnitOfWork = Depends(get_uow)
):
    blocks = []
    for block_id in block_ids:
        block = await uow.blocks.get_unique(BlockWhere(id=block_id))

        if not block or block.profile_id != profile_id:
            raise BlockNotFound()

        blocks.append(block)

    await uow.blocks.delete_many(blocks)
    return None


@blocks_router.delete("/{block_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(can_edit_profile)])
async def delete_block(
    profile_id: UUID,
    block_id: UUID,
    uow: UnitOfWork = Depends(get_uow)
):
    block = await uow.blocks.get_unique(BlockWhere(id=block_id))

    if not block or block.profile_id != profile_id:
        raise BlockNotFound()

    await uow.blocks.delete(block)
    return None


@blocks_router.get("", response_model=None, dependencies=[Depends(get_current_user)])
async def list_blocks(
    profile_id: UUID,
    uow: UnitOfWork = Depends(get_uow)
):
    block_filter = BlockFilter(profile_id=UUIDFilter(eq=profile_id))
    paginated_response = await uow.blocks.list(filter=block_filter, pagination=None)
    return paginated_response


@blocks_router.get("/{block_id}", response_model=Block, dependencies=[Depends(get_current_user)])
async def get_block(
    profile_id: UUID,
    block_id: UUID,
    uow: UnitOfWork = Depends(get_uow)
):
    block = await uow.blocks.get_unique(BlockWhere(id=block_id))

    if not block or block.profile_id != profile_id:
        raise BlockNotFound()

    return block
