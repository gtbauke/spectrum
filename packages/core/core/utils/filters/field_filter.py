from datetime import datetime
from typing import Optional, Any
from abc import ABC, abstractmethod
from pydantic import BaseModel

from sqlalchemy.sql import ColumnElement


class ResolvableField[T](ABC):
    @abstractmethod
    def resolve(self, column: ColumnElement[T]) -> list[Any]: ...


class BaseFieldFilter[T](ResolvableField[T], BaseModel):
    eq: Optional[T] = None
    ne: Optional[T] = None
    in_: Optional[list[T]] = None
    not_in: Optional[list[T]] = None
    is_null: Optional[bool] = None

    def resolve(self, column: ColumnElement[T]):
        conditions: list[ColumnElement[bool]] = []

        if self.eq is not None:
            conditions.append(column == self.eq)

        if self.ne is not None:
            conditions.append(column != self.ne)

        if self.in_ is not None:
            conditions.append(column.in_(self.in_))

        if self.not_in is not None:
            conditions.append(column.not_in(self.not_in))

        if self.is_null is not None:
            if self.is_null:
                conditions.append(column.is_(None))
            else:
                conditions.append(column.is_not(None))

        return conditions


class NumberFilter[T](BaseFieldFilter[T]):
    gt: Optional[T] = None
    gte: Optional[T] = None
    lt: Optional[T] = None
    lte: Optional[T] = None

    def resolve(self, column: ColumnElement[T]):
        conditions = super().resolve(column)

        if self.gt is not None:
            conditions.append(column > self.gt)

        if self.gte is not None:
            conditions.append(column >= self.gte)

        if self.lt is not None:
            conditions.append(column < self.lt)

        if self.lte is not None:
            conditions.append(column <= self.lte)

        return conditions


class StringFilter(BaseFieldFilter[str]):
    like: Optional[str] = None
    ilike: Optional[str] = None

    def resolve(self, column: ColumnElement[str]):
        conditions = super().resolve(column)

        if self.like is not None:
            conditions.append(column.like(self.like))

        if self.ilike is not None:
            conditions.append(column.ilike(self.ilike))

        return conditions


class BooleanFilter(BaseFieldFilter[bool]):
    pass


class DateTimeFilter(NumberFilter[datetime]):
    pass


class UUIDFilter(BaseFieldFilter[str]):
    pass
