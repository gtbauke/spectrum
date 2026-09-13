import json
from typing import cast, Any
from uuid import UUID
from fastapi import APIRouter, Depends

from app.api.unit_of_work import get_uow
from app.features.profiles.models.errors.model_not_found import ModelNotFound
from app.features.profiles.blocks.inference.domain.where import InferenceResultWhere
from app.core.ports.unit_of_work import UnitOfWork

from app.features.auth.guards.get_current_user import get_current_user

from app.features.profiles.models.domain.model import Model
from app.features.profiles.models.domain.where import ModelWhere, ModelFilter
from app.core.utils.filters.field_filter import UUIDFilter
from app.core.utils.pagination.response import PaginatedResponse
from app.core.utils.pagination.base import Pagination
from app.features.profiles.blocks.inference.domain.prediction_service import PredictionEvaluationService

from app.features.profiles.models.dtos.predict import PredictRequestDto, PredictResponseDto
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


@models_router.post(
    path="/{model_id}/predict",
    response_model=PredictResponseDto,
    dependencies=[Depends(dependency=get_current_user)],
)
async def predict_model(
    profile_id: UUID,
    model_id: UUID,
    request: PredictRequestDto,
    uow: UnitOfWork = Depends(dependency=get_uow),
):
    where = ModelWhere(id=model_id)
    model = await uow.models.get_unique(where=where)

    if not model or model.profile_id != profile_id:
        raise ModelNotFound()

    try:
        expr_uuid = UUID(
            request.expression_id) if request.expression_id else None
    except ValueError:
        expr_uuid = None

    expression_str = ""
    parameters: str | dict[str, Any] = "[]"
    returned_expr_id = ""

    if expr_uuid:
        inference_result = await uow.inference_results.get_unique(
            where=InferenceResultWhere(
                id=expr_uuid,
            )
        )

        if not inference_result:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=404, detail="Inference result UUID not found.")
        expression_str = inference_result.numpy or inference_result.expression
        parameters = inference_result.parameters if inference_result.parameters else "[]"
        returned_expr_id = str(expr_uuid)
    else:
        pareto_front = model.metrics.get(
            "pareto_front", []) if model.metrics else []

        if not pareto_front:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=400, detail="Model has no validated expressions available for prediction.")

        selected_expr = None
        if request.expression_id:
            for row in pareto_front:
                if str(row.get("Id", "")) == request.expression_id:
                    selected_expr = row
                    break

            if not selected_expr:
                from fastapi import HTTPException
                raise HTTPException(
                    status_code=404, detail="Expression ID not found in model pareto front.")
        else:
            selected_expr = pareto_front[0]

        expression_str = selected_expr.get(
            "Numpy", selected_expr.get("Pattern", ""))
        parameters = cast(str, selected_expr.get("Parameters", "[]"))
        returned_expr_id = str(selected_expr.get("Id", ""))

    service = PredictionEvaluationService()

    # We want to perform predictions in order of inputs list
    # Aggregate variables across all dicts into arrays for vectorized evaluation
    n_samples = len(request.inputs)
    if n_samples == 0:
        return PredictResponseDto(expression_id=returned_expr_id, predictions=[])

    variables: dict[str, list[float]] = {}

    # Gather keys
    keys = request.inputs[0].keys()
    for key in keys:
        variables[key] = [inp.get(key, 0.0) for inp in request.inputs]

    parsed_params: list[float] = []
    if isinstance(parameters, str):
        try:
            loaded = json.loads(parameters)
            parsed_params = [float(x) for x in loaded] if isinstance(loaded, list) else []
        except json.JSONDecodeError:
            parsed_params = []
    elif isinstance(parameters, dict):
        parsed_params = [
            float(value) for value in parameters.values()
        ]

    predictions_array = service.evaluate_expression(
        expression_str, variables, parsed_params)

    return PredictResponseDto(
        expression_id=returned_expr_id,
        predictions=predictions_array.tolist()
    )
