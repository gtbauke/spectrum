from pydantic import BaseModel

import json


class ModelTrainRequestedEvent(BaseModel):
    dataset_id: str
    bucket: str
    key: str
    uploaded_at: str


def parse_event(sqs_body: str) -> ModelTrainRequestedEvent:
    outer = json.loads(sqs_body)
    inner = json.loads(outer["Message"])

    return ModelTrainRequestedEvent(
        dataset_id=inner["datasetId"],
        bucket=inner["bucket"],
        key=inner["key"],
        uploaded_at=inner["uploadedAt"],
    )
