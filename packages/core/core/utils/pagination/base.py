from pydantic import BaseModel, Field
from sqlalchemy import Select
from typing import Tuple

from db.root import RootBase


class Pagination(BaseModel):
    limit: int = Field(
        default=50, ge=1, description="Number of items to return")

    offset: int = Field(default=0, ge=0, description="Number of items to skip")

    def apply[T: RootBase](self, statement: Select[Tuple[T, ...]]):
        return statement.limit(self.limit).offset(self.offset)
