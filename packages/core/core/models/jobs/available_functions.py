from __future__ import annotations
from enum import StrEnum


class AvailableFunctions(StrEnum):
    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"

    POWER = "power"
    POWERABS = "powerabs"
    SQUARE = "square"
    CUBE = "cube"

    SQRT = "sqrt"
    SQRTABS = "sqrtabs"
    CBRT = "cbrt"

    SIN = "sin"
    COS = "cos"
    TAN = "tan"
    ASIN = "asin"
    ACOS = "acos"
    ATAN = "atan"

    SINH = "sinh"
    COSH = "cosh"
    TANH = "tanh"
    ASINH = "asinh"
    ACOSH = "acosh"
    ATANH = "atanh"

    ABS = "abs"
    LOG = "log"
    LOGABS = "logabs"
    EXP = "exp"
    RECIP = "recip"
    AQ = "aq"

    @staticmethod
    def from_list(*functions: AvailableFunctions) -> str:
        return ",".join(functions)

    @staticmethod
    def to_list(functions_str: str) -> list[AvailableFunctions]:
        return [AvailableFunctions(func.strip()) for func in functions_str.split(",")]
