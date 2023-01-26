from typing import Dict, List, Optional

import expr
import statem


environment: Dict[str, int] = {}


def interpret(statements: List[statem.Statem]) -> List[Optional[int]]:
    result: List[Optional[int]] = []

    for statement in statements:
        result += execute(statement)

    return result


def execute(statement: statem.Statem) -> List[Optional[int]]:
    match statement:
        case statem.Block(statements):
            result: List[Optional[int]] = []

            for individual_statement in statements:
                result += execute(individual_statement)

            return result

        case statem.Expression(expression):
            return [evaluate(expression)]

        case statem.Variable(name, initializer):
            value = evaluate(initializer)
            environment[name.text] = value

            return [None]

        case _:
            raise Exception(f"Exhaustive switch error on statement {str(statement)}.")


def evaluate(expression: expr.Expr) -> int | bool:
    match expression:
        case expr.Integer(value):
            return int(value)

        case expr.Name(text):
            return environment[text]

        case expr.Numeric(operator, left, right):
            left_eval = evaluate(left)
            right_eval = evaluate(right)

            return eval(f"{left_eval} {operator.value} {right_eval}")

        case expr.Relational(operator, left, right):
            left_eval = evaluate(left)
            right_eval = evaluate(right)
            relation = "==" if operator.value == "=" else operator.value

            return eval(f"{left_eval} {relation} {right_eval}")

        case _:
            raise Exception(f"Exhaustive switch error on expression {str(expression)}.")
