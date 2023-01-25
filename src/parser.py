from typing import List, Tuple

from expr import Operator
from scanner import TokenType
import expr
import scanner
import statem


def parse(tokens: List[scanner.Token]) -> statem.Statem:
    counter: int = 0

    statement, _ = expression(tokens, counter)
    return statement


def peek(tokens: List[scanner.Token], counter: int, token_type: TokenType) -> bool:
    return tokens[counter].token_type == token_type


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


def expression(tokens: List[scanner.Token], counter: int) -> Tuple[statem.Statem, int]:
    value, counter = term(tokens, counter)
    _, counter = expect(tokens, counter, TokenType.SEMICOLON)

    return statem.Expression(value), counter


def term(tokens: List[scanner.Token], counter: int) -> Tuple[expr.Expr, int]:
    left, counter = factor(tokens, counter)

    while True:
        if peek(tokens, counter, TokenType.PLUS):
            token, counter = expect(tokens, counter, TokenType.PLUS)
            right, counter = factor(tokens, counter)

            left = expr.Numeric(Operator.PLUS, left, right)
            continue

        elif peek(tokens, counter, TokenType.MINUS):
            token, counter = expect(tokens, counter, TokenType.MINUS)
            right, counter = factor(tokens, counter)

            left = expr.Numeric(Operator.MINUS, left, right)
            continue

        break

    return left, counter


def factor(tokens: List[scanner.Token], counter: int) -> Tuple[expr.Expr, int]:
    left, counter = primary(tokens, counter)

    while True:
        if peek(tokens, counter, TokenType.TIMES):
            token, counter = expect(tokens, counter, TokenType.TIMES)
            right, counter = primary(tokens, counter)

            left = expr.Numeric(Operator.TIMES, left, right)
            continue

        break

    return left, counter


def primary(tokens: List[scanner.Token], counter: int) -> Tuple[expr.Expr, int]:
    token, counter = expect(tokens, counter, TokenType.INTEGER)

    return expr.Integer(token.value), counter
