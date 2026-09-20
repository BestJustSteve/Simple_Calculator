import ast
import operator
from collections.abc import Callable

Number = int | float


OPERATORS: dict[
    type[ast.operator] | type[ast.unaryop],
    Callable[..., Number],
] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def evaluate_node(node: ast.AST) -> Number:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Invalid value")

    if isinstance(node, ast.BinOp):
        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        binary_operator_type = type(node.op)

        if binary_operator_type not in OPERATORS:
            raise ValueError("Invalid operator")

        return OPERATORS[binary_operator_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = evaluate_node(node.operand)

        unary_operator_type = type(node.op)

        if unary_operator_type not in OPERATORS:
            raise ValueError("Invalid operator")

        return OPERATORS[unary_operator_type](operand)

    raise ValueError("Invalid expression")


def calculate_expression(expression: str) -> Number:
    expression = expression.strip()

    tree = ast.parse(
        expression,
        mode="eval",
    )

    result = evaluate_node(tree.body)

    if isinstance(result, complex):
        raise TypeError("Complex numbers are not supported")

    return result


def format_number(number: Number) -> Number:
    if isinstance(number, float) and number.is_integer():
        return int(number)

    return number
