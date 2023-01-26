from typing import List
import dataclasses
import enum


class Operator(enum.Enum):
    EQUAL = "="
    GREATER = ">"
    LESS = "<"
    MINUS = "-"
    PLUS = "+"
    TIMES = "*"


class Expr:
    ...


@dataclasses.dataclass
class Name(Expr):
    text: str


@dataclasses.dataclass
class Call(Expr):
    callee: Name
    arguments: List[Expr]


@dataclasses.dataclass
class Integer(Expr):
    value: str


@dataclasses.dataclass
class Numeric(Expr):
    operator: Operator
    left: Expr
    right: Expr


@dataclasses.dataclass
class Relational(Expr):
    operator: Operator
    left: Expr
    right: Expr
