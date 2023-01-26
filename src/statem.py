from typing import List
import dataclasses

import expr


class Statem:
    ...


@dataclasses.dataclass
class Block(Statem):
    statements: List[Statem]


@dataclasses.dataclass
class Expression(Statem):
    expression: expr.Expr


@dataclasses.dataclass
class If(Statem):
    condition: expr.Expr
    then_branch: Block
    else_branch: Block


@dataclasses.dataclass
class Variable(Statem):
    name: expr.Name
    initializer: expr.Expr
