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

    def resolve_unique_value(self):
        present = self.model_dump(exclude_unset=True)

        if len(present) > 1:
            raise ValueError(
                "BaseUniqueWhere::resolve_unique_value should have only one property")

        if not present:
            raise ValueError(
                "BaseUniqueWhere::resolve_unique_value requires exactly one property to be set")

        _, value = next(iter(present.items()))
        return value
