from typing import List, Optional

import interpreter
import parser
import scanner


def execute(source: str) -> List[Optional[int]]:
    tokens = scanner.scan(source)
    statement = parser.parse(tokens)
    return interpreter.interpret(statement)


def test_integer() -> None:
    assert execute("1;") == [1]

    assert execute("2 + 3;") == [5]
