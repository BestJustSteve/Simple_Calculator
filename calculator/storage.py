import json
import os
from pathlib import Path

APP_NAME = "SimpleCalculator"


def get_data_file():
    if os.name == "nt":
        base_dir = Path(os.environ.get("LOCALAPPDATA", Path.home()))
    else:
        base_dir = Path.home() / ".local" / "share"

    app_dir = base_dir / APP_NAME
    app_dir.mkdir(parents=True, exist_ok=True)

    return app_dir / "calculator_data.json"


DATA_FILE = get_data_file()


def load_data(file_path=DATA_FILE):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        history = data.get("history", [])

        memory = data.get("memory", {})

        last_result = data.get("last_result")

        return (history, memory, last_result)

    except FileNotFoundError:
        return [], {}, None

    except json.JSONDecodeError:
        return [], {}, None


def save_data(history, memory, last_result, file_path=DATA_FILE):
    data = {"history": history, "memory": memory, "last_result": last_result}

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
