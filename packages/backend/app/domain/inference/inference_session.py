from app.domain.models.model import Model
from app.domain.inference.live_model import LiveModel
from app.domain.inference.messages.base import BaseInferenceMessage, BaseInferenceResponse
from app.domain.inference.messages.top_expressions_message import TopExpressionsMessage, TopExpressionsResponse


class InferenceSession:
    def __init__(self, model: Model, live_model: LiveModel):
        self._model = model
        self._live_model = live_model

    async def _handle_top_expressions(self, message: TopExpressionsMessage) -> TopExpressionsResponse:
        top_expressions = self._live_model._egg.top(  # type: ignore
            n=message.topN,
        )

        return TopExpressionsResponse(
            original_message_type="top_expressions",
            res=top_expressions.to_dict(orient="records")  # type: ignore
        )

    async def handle(self, message: BaseInferenceMessage, raw_message: str) -> BaseInferenceResponse:
        match message.message_type:
            case "top_expressions":
                return await self._handle_top_expressions(TopExpressionsMessage.model_validate(raw_message))
            case _:
                raise ValueError(
                    f"Unknown message type: {message.message_type}")
