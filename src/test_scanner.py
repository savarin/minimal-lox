from scanner import TokenType
import scanner


def test_scan() -> None:
    tokens = scanner.scan("1;")

    assert tokens[0] == scanner.Token(TokenType.INTEGER, "1", 1)
    assert tokens[1] == scanner.Token(TokenType.SEMICOLON, ";", 1)
    assert tokens[2] == scanner.Token(TokenType.EOF, "EOF", 1)

    tokens = scanner.scan("2 + 3;")

    assert tokens[0] == scanner.Token(TokenType.INTEGER, "2", 1)
    assert tokens[1] == scanner.Token(TokenType.PLUS, "+", 1)
    assert tokens[2] == scanner.Token(TokenType.INTEGER, "3", 1)
    assert tokens[3] == scanner.Token(TokenType.SEMICOLON, ";", 1)
    assert tokens[4] == scanner.Token(TokenType.EOF, "EOF", 1)

    tokens = scanner.scan("var a = 1;")

    assert tokens[0] == scanner.Token(TokenType.VAR, "var", 1)
    assert tokens[1] == scanner.Token(TokenType.NAME, "a", 1)
    assert tokens[2] == scanner.Token(TokenType.EQUAL, "=", 1)
    assert tokens[3] == scanner.Token(TokenType.INTEGER, "1", 1)
    assert tokens[4] == scanner.Token(TokenType.SEMICOLON, ";", 1)
    assert tokens[5] == scanner.Token(TokenType.EOF, "EOF", 1)

    tokens = scanner.scan("var a = 1; a;")

    assert tokens[0] == scanner.Token(TokenType.VAR, "var", 1)
    assert tokens[1] == scanner.Token(TokenType.NAME, "a", 1)
    assert tokens[2] == scanner.Token(TokenType.EQUAL, "=", 1)
    assert tokens[3] == scanner.Token(TokenType.INTEGER, "1", 1)
    assert tokens[4] == scanner.Token(TokenType.SEMICOLON, ";", 1)
    assert tokens[5] == scanner.Token(TokenType.NAME, "a", 1)
    assert tokens[6] == scanner.Token(TokenType.SEMICOLON, ";", 1)
    assert tokens[7] == scanner.Token(TokenType.EOF, "EOF", 1)
