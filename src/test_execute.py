from scanner import TokenType
import interpreter
import parser
import scanner
import statem


def execute(source: str) -> statem.Statem:
    tokens = scanner.scan(source)
    statement = parser.parse(tokens)
    return interpreter.interpret(statement)


def test_integer() -> None:
    result = execute("1;")

    assert result == 1