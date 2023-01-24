import dataclasses


class Expr:
    ...


@dataclasses.dataclass
class Integer(Expr):
    value: str
