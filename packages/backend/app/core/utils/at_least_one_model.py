from __future__ import annotations
from pydantic import BaseModel, model_validator


class AtLeastOneModelError(ValueError):
    def __init__(self):
        super().__init__(
            "At least one field must be provided, but none were given."
        )


class AtLeastOneModel(BaseModel):
    @model_validator(mode="after")
    def _check_at_least_one(self):
        present = self.model_dump(exclude_unset=True)

        if len(present) == 0:
            raise AtLeastOneModelError()

        return self
