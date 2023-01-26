from typing import Dict, List, Optional
import dataclasses

import expr
import statem


@dataclasses.dataclass
class Return(Exception):
    value: Optional[int]


environment: Dict[str, int | statem.Function] = {}


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
            expression_eval = evaluate(expression)
            assert not isinstance(expression_eval, statem.Function)

            return [expression_eval]

        case statem.Function(name, _, _):
            environment[name.text] = statement

            return [None]

        case statem.If(condition, then_branch, else_branch):
            if_eval = evaluate(condition)

            if if_eval is True:
                return execute(then_branch)

            elif else_branch is not None:
                return execute(else_branch)

            return []

        case statem.Return(expression):
            return_eval = evaluate(expression)
            assert not isinstance(return_eval, statem.Function)

            raise Return(return_eval)

        case statem.Variable(name, initializer):
            variable_eval = evaluate(initializer)
            environment[name.text] = variable_eval

            return [None]

        case _:
            raise Exception(f"Exhaustive switch error on statement {str(statement)}.")


def evaluate(expression: expr.Expr) -> int | bool | statem.Function:
    match expression:
        case expr.Call(callee, arguments):
            call_eval = evaluate(callee)
            args: List[int] = []

            for argument in arguments:
                argument_eval = evaluate(argument)
                assert isinstance(argument_eval, int)

                args.append(argument_eval)

            assert isinstance(call_eval, statem.Function)
            return call(call_eval, args)

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


def call(callee: statem.Function, arguments: List[int]) -> int:
    for i, parameter in enumerate(callee.parameters):
        environment[parameter.text] = arguments[i]

    try:
        execute(callee.body)

    except Return as return_value:
        result = return_value.value

    for parameter in callee.parameters:
        del environment[parameter.text]

    assert isinstance(result, int)
    return result
