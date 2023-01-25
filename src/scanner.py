from typing import Dict, List
import dataclasses
import enum


class TokenType(enum.Enum):
    # Types
    INTEGER = "INTEGER"

    # Single-character tokens.
    EQUAL = "EQUAL"
    MINUS = "MINUS"
    PLUS = "PLUS"
    SEMICOLON = "SEMICOLON"
    TIMES = "TIMES"

    # Keywords
    NAME = "NAME"
    VAR = "VAR"

    EOF = "EOF"


literals: Dict[str, TokenType] = {
    "=": TokenType.EQUAL,
    "-": TokenType.MINUS,
    "+": TokenType.PLUS,
    ";": TokenType.SEMICOLON,
    "*": TokenType.TIMES,
}


keywords: Dict[str, TokenType] = {"var": TokenType.VAR}


@dataclasses.dataclass
class Token:
    token_type: TokenType
    value: str
    line: int


def scan(source: str) -> List[Token]:
    tokens: List[Token] = []
    counter: int = 0
    line: int = 1

    while counter < len(source):
        # Line numbers.
        if source[counter] == "\n":
            counter += 1
            line += 1

        # Whitespace
        elif source[counter].isspace():
            counter += 1

        # Names
        elif source[counter].isalpha():
            start = counter

            while counter < len(source) and source[counter].isalpha():
                counter += 1

            name = source[start:counter]
            token_type = keywords.get(name, TokenType.NAME)

            tokens.append(Token(token_type, name, line))

        # Integers
        elif source[counter].isdigit():
            start = counter

            while counter < len(source) and source[counter].isdigit():
                counter += 1

            tokens.append(Token(TokenType.INTEGER, source[start:counter], line))

        elif source[counter] in literals:
            tokens.append(Token(literals[source[counter]], source[counter], line))
            counter += 1

        else:
            raise Exception(f"Exhaustive switch error on character {source[counter]}.")

    return tokens + [Token(TokenType.EOF, "EOF", line)]
