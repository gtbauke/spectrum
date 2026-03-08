from __future__ import annotations

import logging

from typing import Optional, Union

from sqlalchemy import and_, or_, not_
from sqlalchemy.sql import ColumnElement

from pydantic import BaseModel
from db.root import RootBase

from .field_filter import BaseFieldFilter


logger = logging.getLogger(__name__)


class BaseFilter(BaseModel):
    AND: Optional[list[BaseFilter]] = None
    OR: Optional[list[BaseFilter]] = None
    NOT: Optional[BaseFilter] = None

    def resolve(self, model: Union[type[BaseModel], type[RootBase]]) -> list[ColumnElement[bool]]:
        conditions: list[ColumnElement[bool]] = []

        values = {
            k: getattr(self, k)
            for k in self.model_fields_set
        }

        logger.info("RESOLVING FILTER", extra={
            "model_name": model.__name__,
            "filter_data": self.model_dump(exclude_unset=True, mode="python"),
            "values": values,
        })

        for field, value in values.items():
            logger.info("RESOLVING FILTER FIELD", extra={
                "model_name": model.__name__,
                "field": field,
                "value": value,
                "contains": hasattr(model, field),
            })

            if field == "AND":
                nested = [
                    and_(*f.resolve(model))
                    for f in value
                ]

                conditions.append(and_(*nested))
            elif field == "OR":
                nested = [
                    or_(*f.resolve(model))
                    for f in value
                ]

                conditions.append(or_(*nested))
            elif field == "NOT":
                conditions.append(
                    not_(and_(*value.resolve(model)))
                )
            else:
                if not hasattr(model, field):
                    raise TypeError(
                        f"Model '{model.__name__}' has no field '{field}'")

                column = getattr(model, field)

                if isinstance(value, BaseFieldFilter):
                    conditions.extend(value.resolve(column))  # type: ignore
                elif isinstance(value, BaseFilter):
                    related_model = column.property.mapper.class_
                    nested_conditions = value.resolve(related_model)

                    if column.property.uselist:
                        conditions.append(
                            column.any(and_(*nested_conditions))
                        )
                    else:
                        conditions.append(
                            column.has(and_(*nested_conditions))
                        )
                else:
                    raise TypeError(
                        f"Invalid filter value for field '{field}': {value}"
                    )

        return conditions


BaseFilter.model_rebuild()
