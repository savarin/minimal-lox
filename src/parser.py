from typing import List, Tuple

from scanner import TokenType
import expr
import scanner
import statem


def parse(tokens: List[scanner.Token]) -> statem.Statem:
    counter: int = 0

    statement, _ = expression(tokens, counter)
    return statement


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
    value, counter = integer(tokens, counter)
    _, counter = expect(tokens, counter, TokenType.SEMICOLON)

    return statem.Expression(value), counter


def integer(tokens: List[scanner.Token], counter: int) -> Tuple[expr.Expr, int]:
    token, counter = expect(tokens, counter, TokenType.INTEGER)

    return expr.Integer(token.value), counter
