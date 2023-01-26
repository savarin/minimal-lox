from expr import Operator
from scanner import TokenType
import expr
import scanner
import statem
import parser


def test_parse() -> None:
    tokens = [
        scanner.Token(TokenType.INTEGER, "1", 1),
        scanner.Token(TokenType.SEMICOLON, ";", 1),
        scanner.Token(TokenType.EOF, "EOF", 1),
    ]

    assert parser.parse(tokens) == [statem.Expression(expr.Integer("1"))]

    tokens = [
        scanner.Token(TokenType.INTEGER, "2", 1),
        scanner.Token(TokenType.PLUS, "+", 1),
        scanner.Token(TokenType.INTEGER, "3", 1),
        scanner.Token(TokenType.SEMICOLON, ";", 1),
        scanner.Token(TokenType.EOF, "EOF", 1),
    ]

    assert parser.parse(tokens) == [
        statem.Expression(
            expr.Numeric(Operator.PLUS, expr.Integer("2"), expr.Integer("3"))
        )
    ]

    tokens = [
        scanner.Token(TokenType.VAR, "var", 1),
        scanner.Token(TokenType.NAME, "a", 1),
        scanner.Token(TokenType.EQUAL, "=", 1),
        scanner.Token(TokenType.INTEGER, "1", 1),
        scanner.Token(TokenType.SEMICOLON, ";", 1),
        scanner.Token(TokenType.EOF, "EOF", 1),
    ]

    assert parser.parse(tokens) == [statem.Variable(expr.Name("a"), expr.Integer("1"))]

    tokens = [
        scanner.Token(TokenType.VAR, "var", 1),
        scanner.Token(TokenType.NAME, "a", 1),
        scanner.Token(TokenType.EQUAL, "=", 1),
        scanner.Token(TokenType.INTEGER, "1", 1),
        scanner.Token(TokenType.SEMICOLON, ";", 1),
        scanner.Token(TokenType.NAME, "a", 1),
        scanner.Token(TokenType.SEMICOLON, ";", 1),
        scanner.Token(TokenType.EOF, "EOF", 1),
    ]

    assert parser.parse(tokens) == [
        statem.Variable(expr.Name("a"), expr.Integer("1")),
        statem.Expression(expr.Name("a")),
    ]

    tokens = [
        scanner.Token(TokenType.INTEGER, "0", 1),
        scanner.Token(TokenType.EQUAL, "=", 1),
        scanner.Token(TokenType.INTEGER, "1", 1),
        scanner.Token(TokenType.SEMICOLON, ";", 1),
        scanner.Token(TokenType.EOF, "EOF", 1),
    ]

    assert parser.parse(tokens) == [
        statem.Expression(
            expr.Relational(Operator.EQUAL, expr.Integer("0"), expr.Integer("1"))
        )
    ]

    tokens = [
        scanner.Token(TokenType.IF, "if", 1),
        scanner.Token(TokenType.PAREN_LEFT, "(", 1),
        scanner.Token(TokenType.INTEGER, "0", 1),
        scanner.Token(TokenType.EQUAL, "=", 1),
        scanner.Token(TokenType.INTEGER, "1", 1),
        scanner.Token(TokenType.PAREN_RIGHT, ")", 1),
        scanner.Token(TokenType.BRACE_LEFT, "{", 1),
        scanner.Token(TokenType.INTEGER, "2", 1),
        scanner.Token(TokenType.SEMICOLON, ";", 1),
        scanner.Token(TokenType.BRACE_RIGHT, "}", 1),
        scanner.Token(TokenType.ELSE, "else", 1),
        scanner.Token(TokenType.BRACE_LEFT, "{", 1),
        scanner.Token(TokenType.INTEGER, "3", 1),
        scanner.Token(TokenType.SEMICOLON, ";", 1),
        scanner.Token(TokenType.BRACE_RIGHT, "}", 1),
        scanner.Token(TokenType.EOF, "EOF", 1),
    ]

    assert parser.parse(tokens) == [
        statem.If(
            expr.Relational(Operator.EQUAL, expr.Integer("0"), expr.Integer("1")),
            statem.Block([statem.Expression(expr.Integer("2"))]),
            statem.Block([statem.Expression(expr.Integer("3"))]),
        )
    ]

    tokens = [
        scanner.Token(TokenType.FUNC, "func", 1),
        scanner.Token(TokenType.NAME, "add", 1),
        scanner.Token(TokenType.PAREN_LEFT, "(", 1),
        scanner.Token(TokenType.NAME, "x", 1),
        scanner.Token(TokenType.COMMA, ",", 1),
        scanner.Token(TokenType.NAME, "y", 1),
        scanner.Token(TokenType.PAREN_RIGHT, ")", 1),
        scanner.Token(TokenType.BRACE_LEFT, "{", 1),
        scanner.Token(TokenType.RETURN, "return", 1),
        scanner.Token(TokenType.NAME, "x", 1),
        scanner.Token(TokenType.PLUS, "+", 1),
        scanner.Token(TokenType.NAME, "y", 1),
        scanner.Token(TokenType.SEMICOLON, ";", 1),
        scanner.Token(TokenType.BRACE_RIGHT, "}", 1),
        scanner.Token(TokenType.NAME, "add", 1),
        scanner.Token(TokenType.PAREN_LEFT, "(", 1),
        scanner.Token(TokenType.INTEGER, "2", 1),
        scanner.Token(TokenType.COMMA, ",", 1),
        scanner.Token(TokenType.INTEGER, "3", 1),
        scanner.Token(TokenType.PAREN_RIGHT, ")", 1),
        scanner.Token(TokenType.SEMICOLON, ";", 1),
        scanner.Token(TokenType.EOF, "EOF", 1),
    ]

    assert parser.parse(tokens) == [
        statem.Function(
            expr.Name("add"),
            [expr.Name("x"), expr.Name("y")],
            statem.Block(
                [
                    statem.Return(
                        expr.Numeric(Operator.PLUS, expr.Name("x"), expr.Name("y"))
                    )
                ]
            ),
        ),
        statem.Expression(
            expr.Call(expr.Name("add"), [expr.Integer("2"), expr.Integer("3")]),
        ),
    ]
