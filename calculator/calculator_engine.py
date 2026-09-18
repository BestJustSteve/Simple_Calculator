import ast
import operator


OPERATORS = {
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


def evaluate_node(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Invalid value")

    if isinstance(node, ast.BinOp):
        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        operator_type = type(node.op)

        if operator_type not in OPERATORS:
            raise ValueError("Invalid operator")

        return OPERATORS[operator_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = evaluate_node(node.operand)

        operator_type = type(node.op)

        if operator_type not in OPERATORS:
            raise ValueError("Invalid operator")

        return OPERATORS[operator_type](operand)

    raise ValueError("Invalid expression")


def calculate_expression(expression):
    tree = ast.parse(
        expression,
        mode="eval"
    )

    return evaluate_node(tree.body)


def format_number(number):
    if isinstance(number, float) and number.is_integer():
        return int(number)

    return number