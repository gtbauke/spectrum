from uuid import UUID
from typing import TYPE_CHECKING

from core.utils.filters.field_filter import (
    BooleanFilter, DateTimeFilter, EnumFilter, NumberFilter, StringFilter, UUIDFilter)
from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter

from .available_function import AvailableFunction
from .loss_function import LossFunction

if TYPE_CHECKING:
    from .runs.where import RunFilter
    from core.features.profiles.where import ProfileFilter


class JobWhere(BaseUniqueWhere):
    id: UUID


class JobFilter(BaseFilter):
    id: UUIDFilter | None = None
    name: StringFilter | None = None
    created_at: DateTimeFilter | None = None
    updated_at: DateTimeFilter | None = None
    profile_id: UUIDFilter | None = None
    runs_against: UUIDFilter | None = None
    generations: NumberFilter[int] | None = None
    population: NumberFilter[int] | None = None
    max_size: NumberFilter[int] | None = None
    number_of_tournaments: NumberFilter[int] | None = None
    crossover_probability: NumberFilter[float] | None = None
    mutation_probability: NumberFilter[float] | None = None
    non_terminals: EnumFilter[AvailableFunction] | None = None
    loss: EnumFilter[LossFunction] | None = None
    optimization_iterations: NumberFilter[int] | None = None
    optimization_repeats: NumberFilter[int] | None = None
    max_param_count: NumberFilter[int] | None = None
    split: NumberFilter[int] | None = None
    simplify: BooleanFilter | None = None
    runs: "RunFilter | None" = None
    profile: "ProfileFilter | None" = None
