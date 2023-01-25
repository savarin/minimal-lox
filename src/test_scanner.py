from scanner import TokenType
import scanner


def test_scan() -> None:
    tokens = scanner.scan("1;")

    assert tokens[0] == scanner.Token(TokenType.INTEGER, "1", 1)
    assert tokens[1] == scanner.Token(TokenType.SEMICOLON, ";", 1)
    assert tokens[2] == scanner.Token(TokenType.EOF, "EOF", 1)
