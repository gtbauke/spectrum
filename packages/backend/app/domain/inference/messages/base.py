from pydantic import BaseModel


class BaseInferenceMessage(BaseModel):
    message_type: str


class BaseInferenceResponse(BaseModel):
    original_message_type: str
