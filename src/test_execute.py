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

    result: List[List[Optional[int]]] = []

    for i in range(10):
        source = f"""\
func fibonacci(n) {{
    if (n < 2) {{
        return 1;
    }}

    return fibonacci(n - 1) + fibonacci(n - 2);
}}
fibonacci({i});"""

        result.append(execute(source))

    assert result[0] == [None, 1]
    assert result[1] == [None, 1]
    assert result[2] == [None, 2]
    assert result[3] == [None, 3]
    assert result[4] == [None, 5]
    assert result[5] == [None, 8]
    assert result[6] == [None, 13]
    assert result[7] == [None, 21]
    assert result[8] == [None, 34]
    assert result[9] == [None, 55]
