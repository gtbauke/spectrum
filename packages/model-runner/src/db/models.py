from typing import Optional

from sqlmodel import Session, select
from models import Model, ModelStatus
from db.engine import engine


def get_model_from_id(model_id: str) -> Optional[Model]:
    with Session(engine) as session:
        model = session.get(Model, model_id)
        return model


def get_model_from_dataset_id(dataset_id: str) -> Optional[Model]:
    with Session(engine) as session:
        statement = select(Model).where(Model.dataset_id == dataset_id)
        results = session.exec(statement)
        return results.first()


def update_model_status(model_id: str, new_status: ModelStatus) -> None:
    with Session(engine) as session:
        model = session.get(Model, model_id)

        if model:
            model.status = new_status
            session.add(model)
            session.commit()
