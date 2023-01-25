from expr import Operator
import expr
import formatter
import statem


def test_format() -> None:
    assert formatter.format(statem.Expression(expr.Integer("1"))) == "1;\n"

    assert (
        formatter.format(
            statem.Expression(
                expr.Numeric(Operator.PLUS, expr.Integer("2"), expr.Integer("3"))
            )
        )
        == "2 + 3;\n"
    )

    assert (
        formatter.format(statem.Variable(expr.Name("a"), expr.Integer("1")))
        == "var a = 1;\n"
    )
