from sqlalchemy.orm import DeclarativeBase as Base
from sqlalchemy import and_

from .exactly_one_model import ExactlyOneModel


class BaseUniqueWhere(ExactlyOneModel):
    def resolve(self, model: type[Base]):
        present = self.model_dump(exclude_unset=True)

        filters = [
            getattr(model, field) == value
            for field, value in present.items()
        ]

        return and_(*filters) if len(filters) > 1 else filters[0]
