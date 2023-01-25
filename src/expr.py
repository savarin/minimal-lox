import dataclasses
import enum


class Operator(enum.Enum):
    PLUS = "+"
    MINUS = "-"
    TIMES = "*"


class Expr:
    ...


@dataclasses.dataclass
class Integer(Expr):
    value: str


@dataclasses.dataclass
class Numeric(Expr):
    operator: Operator
    left: Expr
    right: Expr
