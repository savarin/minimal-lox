from typing import Union

import expr
import statem


def format(node: Union[expr.Expr, statem.Statem]) -> str:
    match node:
        case expr.Integer(value):
            return value

        case statem.Expression(expression):
            return f"{format(expression)};\n"

        case _:
            raise Exception(f"Exhaustive switch error on {str(node)}")
