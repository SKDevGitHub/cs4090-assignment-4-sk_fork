# In test_bdd.py (new file!)
import pytest
import json
import os
import sys
from unittest.mock import patch, mock_open
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from tasks import save_tasks, load_tasks, filter_tasks_by_priority, get_overdue_tasks, generate_unique_id
from datetime import datetime

# BDD TEST 1
def test_save_empty_list_creates_empty_json():
    given_tasks = []
    with patch("builtins.open", mock_open()) as mocked_file:
        save_tasks(given_tasks, "mock_tasks.json")
        handle = mocked_file()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        assert written_content == json.dumps([], indent=2)

# BDD TEST 2
def test_filter_high_priority_tasks():
    given_tasks = [
        {"priority": "High"},
        {"priority": "Low"},
        {"priority": "High"},
    ]
    result = filter_tasks_by_priority(given_tasks, "High")
    assert all(task["priority"] == "High" for task in result)
    assert len(result) == 2

# BDD TEST 3
def test_get_overdue_task():
    today = datetime.now().strftime("%Y-%m-%d")
    given_tasks = [
        {"due_date": "2020-01-01", "completed": False},
        {"due_date": today, "completed": False},
    ]
    result = get_overdue_tasks(given_tasks)
    assert any(task["due_date"] == "2020-01-01" for task in result)

# BDD TEST 4
def test_generate_unique_id_is_incremented():
    given_tasks = [{"id": 5}, {"id": 10}]
    result = generate_unique_id(given_tasks)
    assert result == 11

# BDD TEST 5
def test_load_tasks_with_corrupt_json_returns_empty():
    corrupted_json = "{id: 1, title: 'bad}"
    with patch("builtins.open", mock_open(read_data=corrupted_json)):
        result = load_tasks("corrupt.json")
        assert result == []
