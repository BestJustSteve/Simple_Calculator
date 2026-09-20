from calculator.gui_helpers import (
    append_to_display,
    backspace_display,
    build_history_text,
    format_memory_value,
)


def test_append_to_display():
    assert append_to_display("12", "+") == "12+"


def test_append_to_empty_display():
    assert append_to_display("", "7") == "7"


def test_backspace_display():
    assert backspace_display("123") == "12"


def test_backspace_single_character():
    assert backspace_display("7") == ""


def test_backspace_empty_string():
    assert backspace_display("") == ""


def test_format_memory_value_integer():
    assert (
        format_memory_value(
            "answer",
            42,
        )
        == "answer = 42"
    )


def test_format_memory_value_whole_float():
    assert (
        format_memory_value(
            "answer",
            42.0,
        )
        == "answer = 42"
    )


def test_format_memory_value_decimal():
    assert (
        format_memory_value(
            "tax",
            0.08,
        )
        == "tax = 0.08"
    )


def test_empty_history():
    assert build_history_text([]) == "No calculations in history."


def test_build_history_text():
    history = [
        {
            "timestamp": "2026-09-20 12:00:00",
            "expression": "2 + 2",
            "result": 4,
        },
        {
            "timestamp": "2026-09-20 12:01:00",
            "expression": "10 / 4",
            "result": 2.5,
        },
    ]

    result = build_history_text(history)

    assert result == (
        "2026-09-20 12:00:00 | 2 + 2 = 4\n2026-09-20 12:01:00 | 10 / 4 = 2.5"
    )
