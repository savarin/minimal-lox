from typing import Dict, List, Optional, Union
import dataclasses

import expr
import statem


Environment = Dict[str, Union[int, statem.Function, "Environment"]]


@dataclasses.dataclass
class Return(Exception):
    value: Optional[int]


def interpret(statements: List[statem.Statem]) -> List[Optional[int]]:
    environment: Environment = {}
    result: List[Optional[int]] = []

    for statement in statements:
        result += execute(statement, environment)

    return result


def execute(statement: statem.Statem, environment: Environment) -> List[Optional[int]]:
    match statement:
        case statem.Block(statements):
            result: List[Optional[int]] = []

            for individual_statement in statements:
                result += execute(individual_statement, environment)

            return result

        case statem.Expression(expression):
            expression_eval = evaluate(expression, environment)
            assert not isinstance(expression_eval, statem.Function)

            return [expression_eval]

        case statem.Function(name, _, _):
            environment[name.text] = statement

            return [None]

        case statem.If(condition, then_branch, else_branch):
            if_eval = evaluate(condition, environment)

            if if_eval is True:
                return execute(then_branch, environment)

            elif else_branch is not None:
                return execute(else_branch, environment)

            return []

        case statem.Return(expression):
            return_eval = evaluate(expression, environment)
            assert not isinstance(return_eval, statem.Function)

            raise Return(return_eval)

        case statem.Variable(name, initializer):
            variable_eval = evaluate(initializer, environment)
            environment[name.text] = variable_eval

            return [None]

        case _:
            raise Exception(f"Exhaustive switch error on statement {str(statement)}.")


def evaluate(
    expression: expr.Expr, environment: Environment
) -> int | bool | statem.Function:
    match expression:
        case expr.Call(callee, arguments):
            call_eval = evaluate(callee, environment)
            args: List[int] = []

            for argument in arguments:
                argument_eval = evaluate(argument, environment)
                assert isinstance(argument_eval, int)

                args.append(argument_eval)

            assert isinstance(call_eval, statem.Function)
            return call(call_eval, args, environment)

        case expr.Integer(value):
            return int(value)

        case expr.Name(text):
            return get(environment, text)

        case expr.Numeric(operator, left, right):
            left_eval = evaluate(left, environment)
            right_eval = evaluate(right, environment)

            return eval(f"{left_eval} {operator.value} {right_eval}")

        case expr.Relational(operator, left, right):
            left_eval = evaluate(left, environment)
            right_eval = evaluate(right, environment)
            relation = "==" if operator.value == "=" else operator.value

            return eval(f"{left_eval} {relation} {right_eval}")

        case _:
            raise Exception(f"Exhaustive switch error on expression {str(expression)}.")


def get(environment: Environment, name: str) -> int | statem.Function:
    if name in environment:
        value = environment[name]

        assert isinstance(value, int) or isinstance(value, statem.Function)
        return value

    elif "environment" in environment:
        inner = environment["environment"]

        assert not isinstance(inner, int) and not isinstance(inner, statem.Function)
        return get(inner, name)

    raise Exception(f"Name {name} not found across all environments.")


def call(
    callee: statem.Function, arguments: List[int], environment: Environment
) -> int:
    outer: Environment = {"environment": environment}

    for i, parameter in enumerate(callee.parameters):
        outer[parameter.text] = arguments[i]

    try:
        execute(callee.body, outer)

    except Return as return_value:
        result = return_value.value

    assert isinstance(result, int)
    return result
