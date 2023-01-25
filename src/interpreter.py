from typing import Dict, Optional

import expr
import statem


environment: Dict[str, int] = {}


def interpret(statement: statem.Statem) -> Optional[int]:
    match statement:
        case statem.Expression(expression):
            return evaluate(expression)

        case statem.Variable(name, initializer):
            value = evaluate(initializer)
            environment[name.text] = value

            return None

        case _:
            raise Exception(f"Exhaustive switch error on statement {str(statement)}.")


def evaluate(expression: expr.Expr) -> int:
    match expression:
        case expr.Integer(value):
            return int(value)

        case expr.Name(text):
            return environment[text]

        case expr.Numeric(operator, left, right):
            left_eval = evaluate(left)
            right_eval = evaluate(right)

            return eval(f"{left_eval} {operator.value} {right_eval}")

        case _:
            raise Exception(f"Exhaustive switch error on expression {str(expression)}.")
