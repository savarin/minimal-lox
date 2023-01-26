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
    value, counter = relational(tokens, counter)
    _, counter = expect(tokens, counter, TokenType.SEMICOLON)

    return statem.Expression(value), counter


def relational(tokens: List[scanner.Token], counter: int) -> Tuple[expr.Expr, int]:
    left, counter = term(tokens, counter)

    while True:
        if tokens[counter].token_type not in [
            TokenType.EQUAL,
            TokenType.GREATER,
            TokenType.LESS,
        ]:
            break

        operator = Operator(tokens[counter].value)
        counter += 1

        right, counter = term(tokens, counter)
        left = expr.Relational(operator, left, right)

    return left, counter


def term(tokens: List[scanner.Token], counter: int) -> Tuple[expr.Expr, int]:
    left, counter = factor(tokens, counter)

    while True:
        if tokens[counter].token_type not in [TokenType.PLUS, TokenType.MINUS]:
            break

        operator = Operator(tokens[counter].value)
        counter += 1

        right, counter = factor(tokens, counter)
        left = expr.Numeric(operator, left, right)

    return left, counter


def factor(tokens: List[scanner.Token], counter: int) -> Tuple[expr.Expr, int]:
    left, counter = primary(tokens, counter)

    while True:
        if tokens[counter].token_type != TokenType.TIMES:
            break

        operator = Operator(tokens[counter].value)
        counter += 1

        right, counter = primary(tokens, counter)
        left = expr.Numeric(operator, left, right)

    return left, counter


def primary(tokens: List[scanner.Token], counter: int) -> Tuple[expr.Expr, int]:
    match tokens[counter].token_type:
        case TokenType.INTEGER:
            token, counter = expect(tokens, counter, TokenType.INTEGER)
            return expr.Integer(token.value), counter

        case TokenType.NAME:
            token, counter = expect(tokens, counter, TokenType.NAME)
            return expr.Name(token.value), counter

        case _:
            raise Exception(f"Exhaustive switch error on token {tokens[counter]}")
