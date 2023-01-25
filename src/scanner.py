from typing import Dict, List
import dataclasses
import enum


class TokenType(enum.Enum):
    # Single-character tokens.
    SEMICOLON = "SEMICOLON"

    # Keywords
    INTEGER = "INTEGER"

    EOF = "EOF"


literals: Dict[str, TokenType] = {";": TokenType.SEMICOLON}


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
            raise Exception(f"Exhaustive switch error on {source[counter]}")

    return tokens + [Token(TokenType.EOF, "EOF", line)]
