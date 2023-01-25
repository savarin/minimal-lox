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

    assert parser.parse(tokens) == statem.Expression(expr.Integer("1"))

    tokens = [
        scanner.Token(TokenType.INTEGER, "2", 1),
        scanner.Token(TokenType.PLUS, "+", 1),
        scanner.Token(TokenType.INTEGER, "3", 1),
        scanner.Token(TokenType.SEMICOLON, ";", 1),
        scanner.Token(TokenType.EOF, "EOF", 1),
    ]

    assert parser.parse(tokens) == statem.Expression(
        expr.Numeric(Operator.PLUS, expr.Integer("2"), expr.Integer("3"))
    )
