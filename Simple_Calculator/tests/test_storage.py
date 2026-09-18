import json

from calculator.storage import (
    load_data,
    save_data
)


def test_save_and_load_data(tmp_path):
    test_file = tmp_path / "test_data.json"

    history = [
        {
            "timestamp": "2026-09-18 12:00:00",
            "expression": "2 + 2",
            "result": 4
        }
    ]

    memory = {
        "answer": 4
    }

    last_result = 4

    save_data(
        history,
        memory,
        last_result,
        test_file
    )

    loaded_history, loaded_memory, loaded_result = load_data(
        test_file
    )

    assert loaded_history == history
    assert loaded_memory == memory
    assert loaded_result == last_result


def test_load_missing_file(tmp_path):
    test_file = tmp_path / "does_not_exist.json"

    history, memory, last_result = load_data(
        test_file
    )

    assert history == []
    assert memory == {}
    assert last_result is None


def test_load_corrupt_json(tmp_path):
    test_file = tmp_path / "bad_data.json"

    test_file.write_text(
        "{ this is not valid json }"
    )

    history, memory, last_result = load_data(
        test_file
    )

    assert history == []
    assert memory == {}
    assert last_result is None


def test_saved_json_structure(tmp_path):
    test_file = tmp_path / "test_data.json"

    history = []
    memory = {
        "tax": 0.08
    }

    last_result = 25

    save_data(
        history,
        memory,
        last_result,
        test_file
    )

    with open(test_file, "r") as file:
        data = json.load(file)

    assert "history" in data
    assert "memory" in data
    assert "last_result" in data

    assert data["history"] == history
    assert data["memory"] == memory
    assert data["last_result"] == last_result