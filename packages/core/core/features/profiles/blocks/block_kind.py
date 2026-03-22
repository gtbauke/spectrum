from enum import StrEnum
from typing import Literal, Union
from pydantic import BaseModel


class BlockKind(StrEnum):
    MARKDOWN = "markdown"
    INFERENCE = "inference"


class BaseBlock[T](BaseModel):
    data: T


class MarkdownBlock(BaseBlock[str]):
    kind: Literal[BlockKind.MARKDOWN] = BlockKind.MARKDOWN


class InferenceBlock(BaseBlock[str]):
    kind: Literal[BlockKind.INFERENCE] = BlockKind.INFERENCE
