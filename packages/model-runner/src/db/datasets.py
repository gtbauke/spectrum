from typing import Optional

from sqlmodel import Session
from models import Dataset
from db.engine import engine


def get_dataset_from_id(dataset_id: str) -> Optional[Dataset]:
    with Session(engine) as session:
        dataset = session.get(Dataset, dataset_id)
        return dataset
