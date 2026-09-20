from unittest.mock import MagicMock, patch

from calculator.gui import CalculatorApp


class FakeStringVar:
    def __init__(self, value: str = "") -> None:
        self.value = value

    def get(self) -> str:
        return self.value

    def set(self, value: str) -> None:
        self.value = value


def create_app() -> CalculatorApp:
    app = CalculatorApp.__new__(CalculatorApp)

    app.display_var = FakeStringVar()
    app.previous_var = FakeStringVar()

    app.history = []
    app.memory = {}
    app.last_result = None

    return app


def test_button_click():
    app = create_app()

    app.display_var.set("12")

    app.button_click("3")

    assert app.display_var.get() == "123"


def test_clear_display():
    app = create_app()

    app.display_var.set("123")
    app.previous_var.set("1 + 2 =")

    app.clear_display()

    assert app.display_var.get() == ""
    assert app.previous_var.get() == ""


def test_backspace():
    app = create_app()

    app.display_var.set("123")

    app.backspace()

    assert app.display_var.get() == "12"


def test_backspace_empty_display():
    app = create_app()

    app.backspace()

    assert app.display_var.get() == ""


def test_calculate_addition():
    app = create_app()

    app.display_var.set("2 + 3")

    with patch.object(
        app,
        "save",
    ) as mock_save:
        app.calculate()

    assert app.display_var.get() == "5"
    assert app.previous_var.get() == "2 + 3 ="
    assert app.last_result == 5

    assert len(app.history) == 1
    assert app.history[0]["expression"] == "2 + 3"
    assert app.history[0]["result"] == 5

    mock_save.assert_called_once()


def test_calculate_operator_precedence():
    app = create_app()

    app.display_var.set("2 + 3 * 4")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "14"
    assert app.last_result == 14


def test_calculate_decimal():
    app = create_app()

    app.display_var.set("5 / 2")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "2.5"
    assert app.last_result == 2.5


def test_calculate_empty_expression():
    app = create_app()

    with patch.object(
        app,
        "save",
    ) as mock_save:
        app.calculate()

    mock_save.assert_not_called()

    assert app.history == []
    assert app.last_result is None


def test_calculate_division_by_zero():
    app = create_app()

    app.display_var.set("10 / 0")

    with (
        patch("calculator.gui.messagebox.showerror") as mock_error,
        patch.object(
            app,
            "save",
        ) as mock_save,
    ):
        app.calculate()

    mock_error.assert_called_once_with(
        "Error",
        "Cannot divide by zero.",
    )

    mock_save.assert_not_called()

    assert app.history == []
    assert app.last_result is None


def test_calculate_invalid_expression():
    app = create_app()

    app.display_var.set("2 +")

    with (
        patch("calculator.gui.messagebox.showerror") as mock_error,
        patch.object(
            app,
            "save",
        ) as mock_save,
    ):
        app.calculate()

    mock_error.assert_called_once_with(
        "Error",
        "Invalid calculation.",
    )

    mock_save.assert_not_called()


def test_calculate_overflow():
    app = create_app()

    app.display_var.set("10 ** 1000000")

    with (
        patch(
            "calculator.gui.calculate_expression",
            side_effect=OverflowError,
        ),
        patch("calculator.gui.messagebox.showerror") as mock_error,
        patch.object(
            app,
            "save",
        ) as mock_save,
    ):
        app.calculate()

    mock_error.assert_called_once_with(
        "Error",
        "That number is too large.",
    )

    mock_save.assert_not_called()


def test_use_last_result():
    app = create_app()

    app.last_result = 42

    app.use_last_result()

    assert app.display_var.get() == "42"


def test_use_decimal_last_result():
    app = create_app()

    app.last_result = 2.5

    app.use_last_result()

    assert app.display_var.get() == "2.5"


def test_use_last_result_when_none():
    app = create_app()

    with patch("calculator.gui.messagebox.showinfo") as mock_info:
        app.use_last_result()

    mock_info.assert_called_once_with(
        "Last Result",
        "No previous result is available.",
    )

    assert app.display_var.get() == ""


def test_clear_history():
    app = create_app()

    app.history = [
        {
            "timestamp": "2026-09-20 12:00:00",
            "expression": "2 + 2",
            "result": 4,
        }
    ]

    with (
        patch(
            "calculator.gui.messagebox.askyesno",
            return_value=True,
        ),
        patch.object(
            app,
            "save",
        ) as mock_save,
    ):
        app.clear_history()

    assert app.history == []

    mock_save.assert_called_once()


def test_clear_history_cancelled():
    app = create_app()

    app.history = [
        {
            "timestamp": "2026-09-20 12:00:00",
            "expression": "2 + 2",
            "result": 4,
        }
    ]

    with (
        patch(
            "calculator.gui.messagebox.askyesno",
            return_value=False,
        ),
        patch.object(
            app,
            "save",
        ) as mock_save,
    ):
        app.clear_history()

    assert len(app.history) == 1

    mock_save.assert_not_called()


def test_clear_empty_history():
    app = create_app()

    with patch("calculator.gui.messagebox.showinfo") as mock_info:
        app.clear_history()

    mock_info.assert_called_once_with(
        "History",
        "History is already empty.",
    )


def test_load_saved_data():
    app = create_app()

    fake_history = [
        {
            "timestamp": "2026-09-20 12:00:00",
            "expression": "2 + 2",
            "result": 4,
        }
    ]

    fake_memory = {
        "answer": 4,
    }

    fake_last_result = 4

    with patch(
        "calculator.gui.load_data",
        return_value=(
            fake_history,
            fake_memory,
            fake_last_result,
        ),
    ):
        app.load_saved_data()

    assert app.history == fake_history
    assert app.memory == fake_memory
    assert app.last_result == 4


def test_save():
    app = create_app()

    app.history = [
        {
            "timestamp": "2026-09-20 12:00:00",
            "expression": "2 + 2",
            "result": 4,
        }
    ]

    app.memory = {
        "answer": 4,
    }

    app.last_result = 4

    with patch("calculator.gui.save_data") as mock_save_data:
        app.save()

    mock_save_data.assert_called_once_with(
        app.history,
        app.memory,
        app.last_result,
    )


def test_save_oserror():
    app = create_app()

    with (
        patch(
            "calculator.gui.save_data",
            side_effect=OSError,
        ),
        patch("calculator.gui.messagebox.showerror") as mock_error,
    ):
        app.save()

    mock_error.assert_called_once_with(
        "Error",
        "Calculator data could not be saved.",
    )


def test_use_memory_value():
    app = create_app()

    mock_window = MagicMock()

    app.use_memory_value(
        25,
        mock_window,
    )

    assert app.display_var.get() == "25"

    mock_window.destroy.assert_called_once()


def test_use_decimal_memory_value():
    app = create_app()

    mock_window = MagicMock()

    app.use_memory_value(
        2.5,
        mock_window,
    )

    assert app.display_var.get() == "2.5"

    mock_window.destroy.assert_called_once()


def test_delete_memory_value():
    app = create_app()

    app.memory = {
        "tax": 0.08,
    }

    mock_window = MagicMock()

    with (
        patch.object(
            app,
            "save",
        ) as mock_save,
        patch.object(
            app,
            "show_memory",
        ) as mock_show_memory,
    ):
        app.delete_memory_value(
            "tax",
            mock_window,
        )

    assert "tax" not in app.memory

    mock_save.assert_called_once()
    mock_window.destroy.assert_called_once()
    mock_show_memory.assert_called_once()


def test_delete_missing_memory_value():
    app = create_app()

    app.memory = {}

    mock_window = MagicMock()

    with (
        patch.object(
            app,
            "save",
        ) as mock_save,
        patch.object(
            app,
            "show_memory",
        ) as mock_show_memory,
    ):
        app.delete_memory_value(
            "missing",
            mock_window,
        )

    mock_save.assert_not_called()
    mock_window.destroy.assert_not_called()
    mock_show_memory.assert_not_called()


def test_show_history_shortcut():
    app = create_app()

    with patch.object(
        app,
        "show_history",
    ) as mock_method:
        app.show_history_shortcut(
            None,
        )

    mock_method.assert_called_once()


def test_show_memory_shortcut():
    app = create_app()

    with patch.object(
        app,
        "show_memory",
    ) as mock_method:
        app.show_memory_shortcut(
            None,
        )

    mock_method.assert_called_once()


def test_save_memory_shortcut():
    app = create_app()

    with patch.object(
        app,
        "save_last_result_to_memory",
    ) as mock_method:
        app.save_memory_shortcut(
            None,
        )

    mock_method.assert_called_once()


def test_clear_shortcut():
    app = create_app()

    with patch.object(
        app,
        "clear_display",
    ) as mock_method:
        app.clear_shortcut(
            None,
        )

    mock_method.assert_called_once()
