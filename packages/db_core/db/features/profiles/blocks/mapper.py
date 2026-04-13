from db.common.mappers.base import IMapper

from core.features.profiles.blocks.block import Block
from core.features.profiles.blocks.block_kind import BlockKind, MarkdownBlock, InferenceBlock

from .model import BlockORM


class BlockMapper(IMapper[BlockORM, Block]):
    @staticmethod
    def to_domain(orm: BlockORM) -> Block:
        match orm.kind:
            case BlockKind.MARKDOWN:
                data = MarkdownBlock.model_validate(orm.data)
            case BlockKind.INFERENCE:
                data = InferenceBlock.model_validate(orm.data)
                # Populate results and status from the latest inference run if available
                # We expect the repository to have loaded the inference_runs relationship
                latest_run = next(
                    (r for r in orm.inference_runs if r.is_latest), None)
                if latest_run:
                    from db.features.profiles.blocks.inference.mapper import InferenceResultMapper
                    data.status = latest_run.status
                    data.execution_time_ms = latest_run.execution_time_ms
                    data.error = latest_run.error
                    data.results = [InferenceResultMapper.to_domain(
                        r) for r in latest_run.results]
            case _:
                raise ValueError(f"Unknown block kind: {orm.kind}")

        return Block(
            id=orm.id,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            profile_id=orm.profile_id,
            kind=orm.kind,
            order_index=orm.order_index,
            data=data,
        )

    @staticmethod
    def to_orm(domain: Block) -> BlockORM:
        return BlockORM(
            id=domain.id,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            profile_id=domain.profile_id,
            kind=domain.kind,
            order_index=domain.order_index,
            data=domain.data.model_dump() if hasattr(
                domain.data, "model_dump") else domain.data,
        )
