import interpreter
import parser
import scanner


def execute(source: str) -> int:
    tokens = scanner.scan(source)
    statement = parser.parse(tokens)
    return interpreter.interpret(statement)


def test_integer() -> None:
    result = execute("1;")

    assert result == 1
