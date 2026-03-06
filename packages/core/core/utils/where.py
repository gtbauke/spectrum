from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase as Base

from .exactly_one_model import ExactlyOneModel


class BaseUniqueWhere(ExactlyOneModel):
    def resolve(self, model: type[Base]):
        present = self.model_dump(exclude_unset=True)
        condition = next(iter(present.items()))

        return getattr(model, condition[0]) == condition[1]


class BaseFilterWhere(BaseModel):
    def resolve(self, model: type[Base]):
        present = self.model_dump(exclude_unset=True)
        conditions = [getattr(model, key) == value for key,
                      value in present.items()]

        return conditions
