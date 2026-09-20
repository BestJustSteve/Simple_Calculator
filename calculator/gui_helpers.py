from calculator.calculator_engine import Number, format_number
from calculator.storage import History


def build_history_text(history: History) -> str:
    if not history:
        return "No calculations in history."

    lines: list[str] = []

    for entry in history:
        lines.append(
            f"{entry['timestamp']} | "
            f"{entry['expression']} = "
            f"{format_number(entry['result'])}"
        )

    return "\n".join(lines)


def format_memory_value(
    name: str,
    value: Number,
) -> str:
    return f"{name} = {format_number(value)}"


def append_to_display(
    current: str,
    value: str,
) -> str:
    return current + value


def backspace_display(current: str) -> str:
    return current[:-1]
