import expr
import statem


def interpret(statement: statem.Statem) -> int:
    match statement:
        case statem.Expression(expression):
            return evaluate(expression)

        case _:
            raise Exception(f"Exhaustive switch error on statement {str(statement)}.")


def evaluate(expression: expr.Expr) -> int:
    match expression:
        case expr.Integer(value):
            return int(value)

        case expr.Numeric(operator, left, right):
            left_eval = evaluate(left)
            right_eval = evaluate(right)

            return eval(f"{left_eval} {operator.value} {right_eval}")

        case _:
            raise Exception(f"Exhaustive switch error on expression {str(expression)}.")
