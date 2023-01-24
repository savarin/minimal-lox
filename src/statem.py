import dataclasses

import expr


class Statem:
    ...


@dataclasses.dataclass
class Expression(Statem):
    expression: expr.Expr
