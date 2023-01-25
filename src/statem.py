import dataclasses

import expr


class Statem:
    ...


@dataclasses.dataclass
class Expression(Statem):
    expression: expr.Expr


@dataclasses.dataclass
class Variable(Statem):
    name: expr.Name
    initializer: expr.Expr
