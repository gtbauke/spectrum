from core.features.profiles.blocks.inference.inference_run import InferenceRun
from core.features.profiles.blocks.inference.inference_result import InferenceResult
from .model import InferenceRunORM, InferenceResultORM


class InferenceRunMapper:
    @staticmethod
    def to_domain(orm: InferenceRunORM) -> InferenceRun:
        return InferenceRun(
            id=orm.id,
            version=orm.version,
            timestamp=orm.timestamp,
            is_latest=orm.is_latest,
            block_id=orm.block_id,
            profile_id=orm.profile_id,
            query=orm.query,
            status=orm.status,
            execution_time_ms=orm.execution_time_ms,
            error=orm.error
        )

    @staticmethod
    def to_orm(domain: InferenceRun) -> InferenceRunORM:
        return InferenceRunORM(
            id=domain.id,
            version=domain.version,
            timestamp=domain.timestamp,
            is_latest=domain.is_latest,
            block_id=domain.block_id,
            profile_id=domain.profile_id,
            query=domain.query,
            status=domain.status,
            execution_time_ms=domain.execution_time_ms,
            error=domain.error
        )


class InferenceResultMapper:
    @staticmethod
    def to_domain(orm: InferenceResultORM) -> InferenceResult:
        return InferenceResult(
            id=orm.id,
            timestamp=orm.timestamp,
            run_id=orm.run_id,
            run_version=orm.run_version,
            expression=orm.expression,
            dl=orm.dl,
            fitness=orm.fitness,
            latex=orm.latex,
            numpy=orm.numpy,
            parameters=orm.parameters,
            size=orm.size,
            frequency=orm.frequency,
        )

    @staticmethod
    def to_orm(domain: InferenceResult) -> InferenceResultORM:
        return InferenceResultORM(
            id=domain.id,
            timestamp=domain.timestamp,
            run_id=domain.run_id,
            run_version=domain.run_version,
            expression=domain.expression,
            dl=domain.dl,
            fitness=domain.fitness,
            latex=domain.latex,
            numpy=domain.numpy,
            parameters=domain.parameters,
            size=domain.size,
            frequency=domain.frequency
        )
