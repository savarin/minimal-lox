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

    assert (
        formatter.format(
            statem.Expression(
                expr.Relational(Operator.EQUAL, expr.Integer("0"), expr.Integer("1"))
            )
        )
        == "0 = 1;\n"
    )

    assert (
        formatter.format(
            statem.If(
                expr.Relational(Operator.EQUAL, expr.Integer("0"), expr.Integer("1")),
                statem.Block([statem.Expression(expr.Integer("2"))]),
                statem.Block([statem.Expression(expr.Integer("3"))]),
            )
        )
        == """\
if (0 = 1) {
    2;
} else {
    3;
}
"""
    )

    assert (
        formatter.format(
            statem.Function(
                expr.Name("add"),
                [expr.Name("x"), expr.Name("y")],
                statem.Block(
                    [
                        statem.Return(
                            expr.Numeric(Operator.PLUS, expr.Name("x"), expr.Name("y"))
                        )
                    ]
                ),
            )
        )
        == """\
func add(x, y) {
    return x + y;
}
"""
    )

    assert (
        formatter.format(
            statem.Expression(
                expr.Call(expr.Name("add"), [expr.Integer("2"), expr.Name("3")])
            )
        )
        == """add(2, 3);\n"""
    )
