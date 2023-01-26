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

    assert execute("var a = 1; a;") == [None, 1]

    assert execute("0 = 1;") == [False]

    assert execute("if (0 = 1) {2;} else {3;}") == [3]

    assert execute("func add(x, y) { return x + y; } add(2, 3);") == [None, 5]
