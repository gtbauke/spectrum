from __future__ import annotations

from enum import StrEnum
from typing import Any
from pydantic import BaseModel, Field


class PlanNodeKind(StrEnum):
    """Discriminator for every ``LogicalPlanNode`` subclass."""
    SCAN = "scan"
    FILTER = "filter"
    SEARCH = "search"
    PROJECT = "project"
    APPLY = "apply"


class SearchMode(StrEnum):
    """The different retrieval strategies IQL supports."""
    TOP_N = "top_n"
    PARETO = "pareto"
    DISTRIBUTION = "distribution"


class LogicalPlanNode(BaseModel):
    """Abstract base for all nodes in a ``LogicalPlan`` tree.

    Each concrete subclass MUST set its ``kind`` discriminator.
    The ``child`` field creates the tree structure: every node can
    have at most one input child (linear pipeline).
    """
    kind: PlanNodeKind
    child: LogicalPlanNode | None = None

    model_config = {"frozen": True}


class ScanNode(LogicalPlanNode):
    """Represents binding an execution to a specific model / Reggression."""
    kind: PlanNodeKind = Field(default=PlanNodeKind.SCAN)
    model_name: str
    description: str = "Bind to model"


class FilterNode(LogicalPlanNode):
    """Represents a WHERE clause – a list of condition strings."""
    kind: PlanNodeKind = Field(default=PlanNodeKind.FILTER)
    conditions: list[str] = Field(default_factory=list)
    description: str = "Apply filters"


class SearchNode(LogicalPlanNode):
    """Represents the search / retrieval strategy (TOP N, PARETO, DISTRIBUTION)."""
    kind: PlanNodeKind = Field(default=PlanNodeKind.SEARCH)
    mode: SearchMode
    n: int | None = None
    pattern: str | None = None
    at_least: int | None = None
    limit: int | None = None
    description: str = "Search models"


class ProjectNode(LogicalPlanNode):
    """Represents the final column projection (SELECT columns)."""
    kind: PlanNodeKind = Field(default=PlanNodeKind.PROJECT)
    columns: list[str] = Field(default_factory=list)
    description: str = "Select columns"


class ApplyNode(LogicalPlanNode):
    """Represents a function application (e.g. PREDICT)."""
    kind: PlanNodeKind = Field(default=PlanNodeKind.APPLY)
    function_name: str
    arguments: dict[str, float] = Field(default_factory=dict)
    description: str = "Apply function"


class LogicalPlan(BaseModel):
    """A serializable execution plan composed of a tree of ``LogicalPlanNode``s.

    The ``root`` is the outermost operator (typically ``ProjectNode``).
    Reading the tree from root to leaves mirrors the execution order
    bottom-up: leaves run first, results flow upward.
    """
    root: LogicalPlanNode

    model_config = {"frozen": True}

    def to_serializable(self) -> dict:
        """Dump the plan to a JSON-compatible dict for frontend rendering."""
        return self.model_dump(mode="json")
