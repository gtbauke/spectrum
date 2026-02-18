from __future__ import annotations
from pydantic import BaseModel, model_validator


class ExactlyOneModelError(ValueError):
    def __init__(self):
        super().__init__(
            "Exactly one field must be provided, but either none or more than one were given."
        )


class ExactlyOneModel(BaseModel):
    @model_validator(mode="after")
    def _check_exactly_one(self):
        present = self.model_dump(exclude_unset=True)

        if len(present) != 1:
            raise ExactlyOneModelError()

        return self
