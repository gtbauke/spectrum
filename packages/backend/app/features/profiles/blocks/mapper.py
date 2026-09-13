from app.core.database.mappers.base import IMapper

from app.features.profiles.blocks.domain.block import Block
from app.features.profiles.blocks.domain.block_kind import BlockKind, MarkdownBlock, InferenceBlock

from .model import BlockORM


class BlockMapper(IMapper[BlockORM, Block]):
    @staticmethod
    def to_domain(orm: BlockORM) -> Block:
        data: MarkdownBlock | InferenceBlock
        match orm.kind:
            case BlockKind.MARKDOWN:
                data = MarkdownBlock.model_validate(orm.data)
            case BlockKind.INFERENCE:
                inference_data = InferenceBlock.model_validate(orm.data)
                # Populate results and status from the latest inference run if available
                # We expect the repository to have loaded the inference_runs relationship
                latest_run = next(
                    (r for r in orm.inference_runs if r.is_latest), None)
                if latest_run:
                    from app.features.profiles.blocks.inference.mapper import InferenceResultMapper
                    inference_data.status = latest_run.status
                    inference_data.execution_time_ms = latest_run.execution_time_ms
                    inference_data.error = latest_run.error
                    inference_data.results = [InferenceResultMapper.to_domain(
                        r) for r in latest_run.results]
                data = inference_data
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
