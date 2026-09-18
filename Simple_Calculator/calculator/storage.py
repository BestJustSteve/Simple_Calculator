import json


DATA_FILE = "calculator_data.json"


def load_data(file_path=DATA_FILE):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        history = data.get("history", [])
        memory = data.get("memory", {})
        last_result = data.get("last_result")

        return history, memory, last_result

    except FileNotFoundError:
        return [], {}, None

    except json.JSONDecodeError:
        return [], {}, None


def save_data(
    history,
    memory,
    last_result,
    file_path=DATA_FILE
):
    data = {
        "history": history,
        "memory": memory,
        "last_result": last_result
    }

    with open(file_path, "w") as file:
        json.dump(
            data,
            file,
            indent=4
        )