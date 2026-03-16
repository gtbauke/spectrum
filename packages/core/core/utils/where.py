from sqlalchemy.orm import DeclarativeBase as Base
from sqlalchemy import and_

from .at_least_one_model import AtLeastOneModel


class BaseUniqueWhere(AtLeastOneModel):
    def resolve(self, model: type[Base]):
        present = self.model_dump(exclude_unset=True)

        filters = [
            getattr(model, field) == value
            for field, value in present.items()
        ]

        return filters
