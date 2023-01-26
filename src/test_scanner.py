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

    tokens = scanner.scan("0 = 1;")

    assert tokens[0] == scanner.Token(TokenType.INTEGER, "0", 1)
    assert tokens[1] == scanner.Token(TokenType.EQUAL, "=", 1)
    assert tokens[2] == scanner.Token(TokenType.INTEGER, "1", 1)
    assert tokens[3] == scanner.Token(TokenType.SEMICOLON, ";", 1)
    assert tokens[4] == scanner.Token(TokenType.EOF, "EOF", 1)

    tokens = scanner.scan("if (0 = 1) {2;} else {3;}")

    assert tokens[0] == scanner.Token(TokenType.IF, "if", 1)
    assert tokens[1] == scanner.Token(TokenType.PAREN_LEFT, "(", 1)
    assert tokens[2] == scanner.Token(TokenType.INTEGER, "0", 1)
    assert tokens[3] == scanner.Token(TokenType.EQUAL, "=", 1)
    assert tokens[4] == scanner.Token(TokenType.INTEGER, "1", 1)
    assert tokens[5] == scanner.Token(TokenType.PAREN_RIGHT, ")", 1)
    assert tokens[6] == scanner.Token(TokenType.BRACE_LEFT, "{", 1)
    assert tokens[7] == scanner.Token(TokenType.INTEGER, "2", 1)
    assert tokens[8] == scanner.Token(TokenType.SEMICOLON, ";", 1)
    assert tokens[9] == scanner.Token(TokenType.BRACE_RIGHT, "}", 1)
    assert tokens[10] == scanner.Token(TokenType.ELSE, "else", 1)
    assert tokens[11] == scanner.Token(TokenType.BRACE_LEFT, "{", 1)
    assert tokens[12] == scanner.Token(TokenType.INTEGER, "3", 1)
    assert tokens[13] == scanner.Token(TokenType.SEMICOLON, ";", 1)
    assert tokens[14] == scanner.Token(TokenType.BRACE_RIGHT, "}", 1)
    assert tokens[15] == scanner.Token(TokenType.EOF, "EOF", 1)

    tokens = scanner.scan("func add(x, y) { return x + y; } add(2, 3);")

    assert tokens[0] == scanner.Token(TokenType.FUNC, "func", 1)
    assert tokens[1] == scanner.Token(TokenType.NAME, "add", 1)
    assert tokens[2] == scanner.Token(TokenType.PAREN_LEFT, "(", 1)
    assert tokens[3] == scanner.Token(TokenType.NAME, "x", 1)
    assert tokens[4] == scanner.Token(TokenType.COMMA, ",", 1)
    assert tokens[5] == scanner.Token(TokenType.NAME, "y", 1)
    assert tokens[6] == scanner.Token(TokenType.PAREN_RIGHT, ")", 1)
    assert tokens[7] == scanner.Token(TokenType.BRACE_LEFT, "{", 1)
    assert tokens[8] == scanner.Token(TokenType.RETURN, "return", 1)
    assert tokens[9] == scanner.Token(TokenType.NAME, "x", 1)
    assert tokens[10] == scanner.Token(TokenType.PLUS, "+", 1)
    assert tokens[11] == scanner.Token(TokenType.NAME, "y", 1)
    assert tokens[12] == scanner.Token(TokenType.SEMICOLON, ";", 1)
    assert tokens[13] == scanner.Token(TokenType.BRACE_RIGHT, "}", 1)
    assert tokens[14] == scanner.Token(TokenType.NAME, "add", 1)
    assert tokens[15] == scanner.Token(TokenType.PAREN_LEFT, "(", 1)
    assert tokens[16] == scanner.Token(TokenType.INTEGER, "2", 1)
    assert tokens[17] == scanner.Token(TokenType.COMMA, ",", 1)
    assert tokens[18] == scanner.Token(TokenType.INTEGER, "3", 1)
    assert tokens[19] == scanner.Token(TokenType.PAREN_RIGHT, ")", 1)
    assert tokens[20] == scanner.Token(TokenType.SEMICOLON, ";", 1)
    assert tokens[21] == scanner.Token(TokenType.EOF, "EOF", 1)
