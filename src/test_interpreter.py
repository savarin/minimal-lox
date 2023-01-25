import expr
import interpreter
import statem


def test_interpret() -> None:
    assert interpreter.interpret(statem.Expression(expr.Integer("1"))) == 1
