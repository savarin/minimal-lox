from typing import List, Optional
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
class Function(Statem):
    name: expr.Name
    parameters: List[expr.Name]
    body: Statem


@dataclasses.dataclass
class If(Statem):
    condition: expr.Expr
    then_branch: Statem
    else_branch: Optional[Statem]


@dataclasses.dataclass
class Variable(Statem):
    name: expr.Name
    initializer: expr.Expr


@dataclasses.dataclass
class Return(Statem):
    expression: expr.Expr
