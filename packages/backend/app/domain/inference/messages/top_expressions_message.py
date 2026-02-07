from typing import Any
from pydantic import Field

from app.domain.inference.messages.base import BaseInferenceMessage, BaseInferenceResponse

# TODO: add other parameters to this message, such as filters, etc.


class TopExpressionsMessage(BaseInferenceMessage):
    message_type: str = "top_expressions"
    topN: int = Field(..., description="Number of top expressions to return")


class TopExpressionsResponse(BaseInferenceResponse):
    original_message_type: str = "top_expressions"
    res: list[dict[str, Any]] = Field(...,
                                      description="The result of the top expressions query")
