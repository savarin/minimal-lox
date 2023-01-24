import expr
import formatter
import statem


def test_formatter() -> None:
    assert formatter.format(statem.Expression(expr.Integer("1"))) == "1;\n"
