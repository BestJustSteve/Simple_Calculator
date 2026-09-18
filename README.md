# Simple Calculator

A desktop calculator application built with Python and Tkinter.

The project supports standard arithmetic, operator precedence, parentheses, calculation history, saved memory values, JSON persistence, keyboard shortcuts, CSV export, and automated tests with pytest.

## Features

- Addition, subtraction, multiplication, and division
- Floor division
- Modulus
- Exponents
- Parentheses
- Operator precedence
- Negative numbers
- Decimal calculations
- Calculation history
- Saved memory values
- Last-answer recall
- Persistent JSON storage
- Keyboard shortcuts
- CSV history export
- Safe expression parsing with Python's AST module
- Automated testing with pytest

## Project Structure

```text
Simple_Calculator/
├── calculator/
│   ├── __init__.py
│   ├── calculator_engine.py
│   ├── storage.py
│   └── gui.py
├── tests/
│   ├── test_calculator_engine.py
│   └── test_storage.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.12 or newer
- Tkinter
- pytest for running automated tests

> Tkinter is included with most standard Python installations on Windows.

## Installation

Clone the repository:

```bash
git clone https://github.com/BestJustSteve/Simple_Calculator.git
```

Move into the project directory:

```bash
cd Simple_Calculator
```

Install the required Python packages:

```bash
python -m pip install -r requirements.txt
```

## Running the Calculator

From the project root, run:

```bash
python main.py
```

The calculator desktop window should open.

## Supported Operators

| Operator | Description |
|---|---|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `//` | Floor division |
| `%` | Modulus |
| `**` | Exponent |

### Examples

```text
10 + 5
10 + 5 * 2
(10 + 5) * 2
2 ** 3
10 // 3
10 % 3
```

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Enter` | Calculate |
| `Backspace` | Delete previous character |
| `Escape` | Clear display |
| `Ctrl+H` | View history |
| `Ctrl+M` | View saved memory |
| `Ctrl+S` | Save last result |
| `Ctrl+L` | Clear display |

## Calculation History

Each successful calculation is stored with a timestamp.

Example:

```text
2026-09-18 14:30:00 | 10+5*2 = 20
```

History is stored in:

```text
calculator/calculator_data.json
```

This file is generated automatically and is excluded from Git through `.gitignore`.

## Memory

Results can be stored under custom names.

For example:

```text
tax = 0.08
subtotal = 149.99
```

Saved values can later be inserted into calculations from the Memory window.

## Data Storage

Application data is saved as JSON.

Example:

```json
{
  "history": [
    {
      "timestamp": "2026-09-18 14:30:00",
      "expression": "10+5*2",
      "result": 20
    }
  ],
  "memory": {
    "tax": 0.08
  },
  "last_result": 20
}
```

## Safe Expression Parsing

The calculator does not use Python's built-in `eval()` function.

Instead, expressions are parsed using Python's `ast` module. Only explicitly supported mathematical operations are allowed.

This prevents arbitrary Python code from being executed through calculator input.

## Running Tests

Run all automated tests with:

```bash
python -m pytest
```

For verbose output:

```bash
python -m pytest -v
```

The test suite covers:

- Arithmetic operations
- Operator precedence
- Parentheses
- Negative numbers
- Decimal values
- Division by zero
- Invalid expressions
- Rejection of unsupported Python code
- JSON saving and loading
- Missing data files
- Corrupt JSON data

At the time of this README update, the test suite contains **25 passing tests**.

### Example Test

```python
def test_operator_precedence():
    assert calculate_expression("10 + 5 * 2") == 20
```

## Building a Windows Executable

PyInstaller can be used to build a standalone Windows executable:

```bash
python -m PyInstaller --onefile --windowed --name SimpleCalculator main.py
```

The executable will be created in:

```text
dist/SimpleCalculator.exe
```

The generated `build/`, `dist/`, and `.spec` files are excluded through `.gitignore`.

## Technologies Used

- Python
- Tkinter
- ttk
- AST
- JSON
- CSV
- pytest
- PyInstaller

## Future Improvements

Possible future additions include:

- Improved GUI styling
- Scientific calculator functions
- Dark mode
- Additional history filtering
- Memory editing
- Additional export options
- GitHub Actions automated testing

## Author

Steve Butler
