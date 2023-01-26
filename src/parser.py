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
        case TokenType.BRACE_LEFT:
            return block(tokens, counter)

        case TokenType.FUNC:
            return function(tokens, counter)

        case TokenType.IF:
            return if_statement(tokens, counter)

        case TokenType.VAR:
            return variable(tokens, counter)

        case TokenType.RETURN:
            return return_statement(tokens, counter)

        case TokenType.NAME | TokenType.INTEGER:
            return expression_statement(tokens, counter)

        case _:
            raise Exception(f"Exhaustive switch error on token {tokens[counter]}.")


def block(tokens: List[scanner.Token], counter: int) -> Tuple[statem.Statem, int]:
    # { statements }
    statements: List[statem.Statem] = []

    _, counter = expect(tokens, counter, TokenType.BRACE_LEFT)

    while tokens[counter].token_type != TokenType.BRACE_RIGHT:
        individual_statement, counter = statement(tokens, counter)
        statements.append(individual_statement)

    _, counter = expect(tokens, counter, TokenType.BRACE_RIGHT)

    return statem.Block(statements), counter


def function(tokens: List[scanner.Token], counter: int) -> Tuple[statem.Statem, int]:
    # func name ( parameters ) { body }
    _, counter = expect(tokens, counter, TokenType.FUNC)
    name, counter = expect(tokens, counter, TokenType.NAME)
    _, counter = expect(tokens, counter, TokenType.PAREN_LEFT)

    parameters: List[expr.Name] = []

    while tokens[counter].token_type != TokenType.PAREN_RIGHT:
        parameter, counter = expect(tokens, counter, TokenType.NAME)
        parameters.append(expr.Name(parameter.value))

        if tokens[counter].token_type == TokenType.COMMA:
            _, counter = expect(tokens, counter, TokenType.COMMA)

    _, counter = expect(tokens, counter, TokenType.PAREN_RIGHT)
    body, counter = block(tokens, counter)

    assert isinstance(body, statem.Block)
    return statem.Function(expr.Name(name.value), parameters, body), counter


def if_statement(
    # if ( condition ) { then_branch } [ else_branch ]
    tokens: List[scanner.Token],
    counter: int,
) -> Tuple[statem.Statem, int]:
    _, counter = expect(tokens, counter, TokenType.IF)
    _, counter = expect(tokens, counter, TokenType.PAREN_LEFT)
    condition, counter = expression(tokens, counter)
    _, counter = expect(tokens, counter, TokenType.PAREN_RIGHT)
    then_branch, counter = block(tokens, counter)

    else_branch = None

    if tokens[counter].token_type == TokenType.ELSE:
        _, counter = expect(tokens, counter, TokenType.ELSE)
        else_branch, counter = block(tokens, counter)

    assert isinstance(then_branch, statem.Block)
    assert isinstance(else_branch, statem.Block) or else_branch is None
    return statem.If(condition, then_branch, else_branch), counter


def variable(tokens: List[scanner.Token], counter: int) -> Tuple[statem.Statem, int]:
    # var name initializer ;
    _, counter = expect(tokens, counter, TokenType.VAR)
    name, counter = expect(tokens, counter, TokenType.NAME)
    _, counter = expect(tokens, counter, TokenType.EQUAL)
    initializer, counter = expect(tokens, counter, TokenType.INTEGER)
    _, counter = expect(tokens, counter, TokenType.SEMICOLON)

    return (
        statem.Variable(expr.Name(name.value), expr.Integer(initializer.value)),
        counter,
    )


def return_statement(
    # return expression ;
    tokens: List[scanner.Token],
    counter: int,
) -> Tuple[statem.Statem, int]:
    _, counter = expect(tokens, counter, TokenType.RETURN)
    value, counter = expression(tokens, counter)
    _, counter = expect(tokens, counter, TokenType.SEMICOLON)

    return statem.Return(value), counter


def expression_statement(
    # expression ;
    tokens: List[scanner.Token],
    counter: int,
) -> Tuple[statem.Statem, int]:
    value, counter = expression(tokens, counter)
    _, counter = expect(tokens, counter, TokenType.SEMICOLON)

    return statem.Expression(value), counter


def expression(tokens: List[scanner.Token], counter: int) -> Tuple[expr.Expr, int]:
    return relational(tokens, counter)


def relational(tokens: List[scanner.Token], counter: int) -> Tuple[expr.Expr, int]:
    # left = right
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
    # left + right
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
    # left * right
    left, counter = call(tokens, counter)

    while True:
        if tokens[counter].token_type != TokenType.TIMES:
            break

        operator = Operator(tokens[counter].value)
        counter += 1

        right, counter = call(tokens, counter)
        left = expr.Numeric(operator, left, right)

    return left, counter


def call(tokens: List[scanner.Token], counter: int) -> Tuple[expr.Expr, int]:
    # name ( arguments )
    primary_expression, counter = primary(tokens, counter)

    if tokens[counter].token_type != TokenType.PAREN_LEFT:
        return primary_expression, counter

    _, counter = expect(tokens, counter, TokenType.PAREN_LEFT)

    arguments: List[expr.Expr] = []

    while tokens[counter].token_type != TokenType.PAREN_RIGHT:
        argument, counter = expression(tokens, counter)
        arguments.append(argument)

        if tokens[counter].token_type == TokenType.COMMA:
            _, counter = expect(tokens, counter, TokenType.COMMA)

    _, counter = expect(tokens, counter, TokenType.PAREN_RIGHT)

    assert isinstance(primary_expression, expr.Name)
    return expr.Call(primary_expression, arguments), counter


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
