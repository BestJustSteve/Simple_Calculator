import pytest

from calculator.calculator_engine import (
    calculate_expression,
    format_number
)


def test_addition():
    assert calculate_expression("2 + 2") == 4


def test_subtraction():
    assert calculate_expression("10 - 3") == 7


def test_multiplication():
    assert calculate_expression("6 * 4") == 24


def test_division():
    assert calculate_expression("10 / 2") == 5


def test_floor_division():
    assert calculate_expression("10 // 3") == 3


def test_modulus():
    assert calculate_expression("10 % 3") == 1


def test_power():
    assert calculate_expression("2 ** 3") == 8


def test_operator_precedence():
    assert calculate_expression("10 + 5 * 2") == 20


def test_parentheses():
    assert calculate_expression("(10 + 5) * 2") == 30


def test_negative_number():
    assert calculate_expression("-5 + 10") == 5


def test_decimal_math():
    assert calculate_expression("2.5 + 1.5") == 4.0


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate_expression("10 / 0")


def test_invalid_expression():
    with pytest.raises((ValueError, SyntaxError)):
        calculate_expression("hello + 5")


def test_function_call_is_rejected():
    with pytest.raises(ValueError):
        calculate_expression("print('hello')")


def test_format_whole_float():
    assert format_number(10.0) == 10


def test_format_decimal():
    assert format_number(10.5) == 10.5

def test_nested_parentheses():
    assert calculate_expression("((2 + 3) * 4)") == 20


def test_multiple_operations():
    assert calculate_expression("2 + 3 * 4 - 5") == 9


def test_negative_parentheses():
    assert calculate_expression("-(5 + 2)") == -7


def test_decimal_division():
    assert calculate_expression("5 / 2") == 2.5

def test_import_is_rejected():
    with pytest.raises((ValueError, SyntaxError)):
        calculate_expression("__import__('os')")