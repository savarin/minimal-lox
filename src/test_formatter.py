import expr
import formatter
import statem


def test_format() -> None:
    assert formatter.format(statem.Expression(expr.Integer("1"))) == "1;\n"
