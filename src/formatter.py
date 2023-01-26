from typing import Union

import expr
import statem


def format(node: Union[expr.Expr, statem.Statem]) -> str:
    match node:
        case expr.Call(callee, arguments):
            args = ", ".join([f"{format(arg)}" for arg in arguments])

            return f"{format(callee)}({args})"

        case expr.Integer(value):
            return value

        case expr.Name(text):
            return text

        case expr.Numeric(operator, left, right):
            return f"{format(left)} {operator.value} {format(right)}"

        case expr.Relational(operator, left, right):
            return f"{format(left)} {operator.value} {format(right)}"

        case statem.Block(statements):
            result = "{\n    "

            for statement in statements:
                result += format(statement).replace("\n", "\n    ")

            return result.rstrip("    ") + "}\n"

        case statem.Expression(expression):
            return f"{format(expression)};\n"

        case statem.Function(name, parameters, body):
            params = ", ".join([f"{format(parameter)}" for parameter in parameters])

            return f"func {format(name)}({params}) {format(body)}"

        case statem.If(condition, then_branch, else_branch):
            consequent = f"if ({format(condition)}) {format(then_branch)}"

            alternate = (
                f" else {format(else_branch)}" if else_branch is not None else ""
            )

            if else_branch is not None:
                consequent = consequent.rstrip("\n")

            return consequent + alternate

        case statem.Return(expression):
            return f"return {format(expression)};\n"

        case statem.Variable(name, initializer):
            return f"var {format(name)} = {format(initializer)};\n"

        case _:
            raise Exception(f"Exhaustive switch error on {str(node)}")
