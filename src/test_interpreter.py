from expr import Operator
import expr
import interpreter
import statem


def test_interpret() -> None:
    assert interpreter.interpret([statem.Expression(expr.Integer("1"))]) == [1]

    assert interpreter.interpret(
        [
            statem.Expression(
                expr.Numeric(Operator.PLUS, expr.Integer("2"), expr.Integer("3"))
            )
        ]
    ) == [5]
