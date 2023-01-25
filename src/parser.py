from typing import List, Tuple

from expr import Operator
from scanner import TokenType
import expr
import scanner
import statem


def parse(tokens: List[scanner.Token]) -> List[statem.Statem]:
    statements: List[statem.Statem] = []
    counter: int = 0

    while tokens[counter].token_type != TokenType.EOF:
        individual_statement, counter = statement(tokens, counter)
        statements.append(individual_statement)

    return statements


def expect(
    tokens: List[scanner.Token], counter: int, token_type: TokenType
) -> Tuple[scanner.Token, int]:
    token = tokens[counter]
    counter += 1

    if token.token_type == token_type:
        return token, counter

    raise Exception(
        f"Expected token with token type {token_type}, got {token.token_type}"
    )


def statement(tokens: List[scanner.Token], counter: int) -> Tuple[statem.Statem, int]:
    match tokens[counter].token_type:
        case TokenType.VAR:
            return variable(tokens, counter)

        case TokenType.NAME:
            return expression(tokens, counter)

        case TokenType.INTEGER:
            return expression(tokens, counter)

        case _:
            raise Exception(f"Exhaustive switch error on token {tokens[counter]}.")


def variable(tokens: List[scanner.Token], counter: int) -> Tuple[statem.Statem, int]:
    _, counter = expect(tokens, counter, TokenType.VAR)
    name, counter = expect(tokens, counter, TokenType.NAME)
    _, counter = expect(tokens, counter, TokenType.EQUAL)
    initializer, counter = expect(tokens, counter, TokenType.INTEGER)
    _, counter = expect(tokens, counter, TokenType.SEMICOLON)

    return (
        statem.Variable(expr.Name(name.value), expr.Integer(initializer.value)),
        counter,
    )


def expression(tokens: List[scanner.Token], counter: int) -> Tuple[statem.Statem, int]:
    value, counter = term(tokens, counter)
    _, counter = expect(tokens, counter, TokenType.SEMICOLON)

    return statem.Expression(value), counter


def term(tokens: List[scanner.Token], counter: int) -> Tuple[expr.Expr, int]:
    left, counter = factor(tokens, counter)

    while True:
        if tokens[counter].token_type in [TokenType.PLUS, TokenType.MINUS]:
            operator = Operator(tokens[counter].value)
            counter += 1

            right, counter = factor(tokens, counter)
            left = expr.Numeric(operator, left, right)
            continue

        break

    return left, counter


def factor(tokens: List[scanner.Token], counter: int) -> Tuple[expr.Expr, int]:
    left, counter = primary(tokens, counter)

    while True:
        if tokens[counter] == TokenType.TIMES:
            operator = Operator(tokens[counter].value)
            counter += 1

            right, counter = primary(tokens, counter)
            left = expr.Numeric(operator, left, right)
            continue

        break

    return left, counter


def primary(tokens: List[scanner.Token], counter: int) -> Tuple[expr.Expr, int]:
    token, counter = expect(tokens, counter, TokenType.INTEGER)

    return expr.Integer(token.value), counter
