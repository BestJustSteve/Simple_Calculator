import pytest

from calculator.calculator_engine import calculate_expression, format_number


def test_nested_parentheses():
    assert calculate_expression("((2 + 3) * 4)") == 20


def test_multiple_operations():
    assert calculate_expression("2 + 3 * 4 - 5") == 9


def test_negative_parentheses():
    assert calculate_expression("-(5 + 2)") == -7


def test_unary_plus():
    assert calculate_expression("+5") == 5


def test_decimal_division():
    assert calculate_expression("5 / 2") == 2.5


def test_decimal_multiplication():
    assert calculate_expression("2.5 * 4") == 10.0


def test_power_precedence():
    assert calculate_expression("2 + 3 ** 2") == 11


def test_parentheses_override_precedence():
    assert calculate_expression("(2 + 3) ** 2") == 25


def test_floor_division_negative_number():
    assert calculate_expression("-10 // 3") == -4


def test_modulus_negative_number():
    assert calculate_expression("-10 % 3") == 2


def test_empty_expression():
    with pytest.raises(SyntaxError):
        calculate_expression("")


def test_incomplete_expression():
    with pytest.raises(SyntaxError):
        calculate_expression("5 +")


def test_double_operator_invalid():
    with pytest.raises(SyntaxError):
        calculate_expression("5 + * 2")


def test_unknown_name_is_rejected():
    with pytest.raises(ValueError):
        calculate_expression("hello")


def test_function_call_is_rejected():
    with pytest.raises(ValueError):
        calculate_expression("print('hello')")


def test_import_call_is_rejected():
    with pytest.raises(ValueError):
        calculate_expression("__import__('os')")


def test_attribute_access_is_rejected():
    with pytest.raises(ValueError):
        calculate_expression("(1).__class__")


def test_list_is_rejected():
    with pytest.raises(ValueError):
        calculate_expression("[1, 2, 3]")


def test_dictionary_is_rejected():
    with pytest.raises(ValueError):
        calculate_expression("{'a': 1}")


def test_comparison_is_rejected():
    with pytest.raises(ValueError):
        calculate_expression("5 > 2")


def test_boolean_expression_is_rejected():
    with pytest.raises(ValueError):
        calculate_expression("True and False")


def test_string_is_rejected():
    with pytest.raises(ValueError):
        calculate_expression("'hello'")


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate_expression("10 / 0")


def test_floor_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate_expression("10 // 0")


def test_modulus_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate_expression("10 % 0")


def test_format_whole_float():
    assert format_number(10.0) == 10


def test_format_decimal():
    assert format_number(10.25) == 10.25


def test_format_integer():
    assert format_number(10) == 10
