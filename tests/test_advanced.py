import pytest
import sys
import os
import json
from datetime import datetime
from unittest.mock import patch, mock_open
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_completion, generate_unique_id, get_overdue_tasks

@pytest.mark.parametrize("task, expected_priority", [
    ({"id": 1, "title": "Task 1", "priority": "High", "category": "Work", "due_date": "2025-05-01", "completed": False}, "High"),
    ({"id": 2, "title": "Task 2", "priority": "Medium", "category": "Personal", "due_date": "2025-05-02", "completed": False}, "Medium"),
])

def test_task_priority(task, expected_priority):
    assert task["priority"] == expected_priority

# Test cases for advanced task filtering and management functions
@pytest.mark.mock
def test_load_tasks_with_mock():
    mock_data = [
        {"id": 1, "title": "Test Task 1", "priority": "High", "category": "Work", "due_date": "2025-05-01", "completed": False},
        {"id": 2, "title": "Test Task 2", "priority": "Medium", "category": "Personal", "due_date": "2025-05-02", "completed": False}
    ]
    mock_json_data = json.dumps(mock_data)
    with patch("builtins.open", mock_open(read_data = mock_json_data)):
        tasks = load_tasks("mock_tasks.json")
        assert len(tasks) == 2
        assert tasks[0]["title"] == "Test Task 1"


#No Matching Priority
@pytest.mark.mock
def test_filter_tasks_by_priority_no_match():
    mock_data = [
        {"id": 1, "title": "Test Task 1", "priority": "High", "category": "Work", "due_date": "2025-05-01", "completed": False},
        {"id": 2, "title": "Test Task 2", "priority": "Medium", "category": "Personal", "due_date": "2025-05-02", "completed": False}
    ]
    result = filter_tasks_by_priority(mock_data, "Urgent")
    assert result == []

#Filter by completion stautus
@pytest.mark.mock
def test_filter_tasks_by_completion():
    mock_data = [
        {"id": 1, "title": "Test Task 1", "priority": "High", "category": "Work", "due_date": "2025-05-01", "completed": True},
        {"id": 2, "title": "Test Task 2", "priority": "Medium", "category": "Personal", "due_date": "2025-05-02", "completed": False}
    ]
    completed = filter_tasks_by_completion(mock_data, True)
    assert len(completed) == 1
    assert completed[0]["title"] == "Test Task 1"

    incomplete = filter_tasks_by_completion(mock_data, False)
    assert len(incomplete) == 1
    assert incomplete[0]["title"] == "Test Task 2"

# Test case for saving tasks with mock
@pytest.mark.mock
def test_save_tasks_with_mock():
    mock_data = [
        {"id": 1, "title": "Test Task 1", "priority": "High", "category": "Work", "due_date": "2025-05-01", "completed": False},
        {"id": 2, "title": "Test Task 2", "priority": "Medium", "category": "Personal", "due_date": "2025-05-02", "completed": False}
    ]
    with patch("builtins.open", mock_open()) as mocked_file:
        save_tasks(mock_data, "mock_tasks.json")
        handle = mocked_file()
        
        # Collect all writes
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        
        expected_content = json.dumps(mock_data, indent=2)
        
        assert written_content == expected_content

def test_load_tasks_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        tasks = load_tasks("nonexistent_file.json")
        assert tasks == []

def test_load_tasks_json_decode_error():
    corrupted_json = "{id: 1, title: 'Test Task'}"  # Invalid JSON
    with patch("builtins.open", mock_open(read_data=corrupted_json)):
        tasks = load_tasks("corrupted_file.json")
        assert tasks == []

def test_save_empty_task_list():
    with patch("builtins.open", mock_open()) as mocked_file:
        save_tasks([], "mock_tasks.json")
        handle = mocked_file()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        expected_content = json.dumps([], indent=2)
        assert written_content == expected_content

def test_generate_unique_id_no_tasks():
    tasks = []
    new_id = generate_unique_id(tasks)
    assert new_id == 1

def test_generate_unique_id_with_tasks():
    tasks = [{"id": 1}, {"id": 2}]
    new_id = generate_unique_id(tasks)
    assert new_id == 3

def test_filter_tasks_by_priority():
    tasks = [
        {"priority": "High"},
        {"priority": "Low"},
        {"priority": "High"}
    ]
    filtered_tasks = filter_tasks_by_priority(tasks, "High")
    assert len(filtered_tasks) == 2
    assert filtered_tasks[0]["priority"] == "High"

def test_get_overdue_tasks():
    today = datetime.now().strftime("%Y-%m-%d")
    tasks = [
        {"due_date": "2025-01-01", "completed": False},
        {"due_date": "2025-07-01", "completed": False},
        {"due_date": today, "completed": False}
    ]
    overdue_tasks = get_overdue_tasks(tasks)
    assert len(overdue_tasks) == 1  # Only the first task is overdue
    assert overdue_tasks[0]["due_date"] == "2025-01-01"
