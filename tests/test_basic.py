import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category, filter_tasks_by_completion
import json

mock_tasks = [
    {"id": 1, "title": "Test Task 1", "description": "Description 1", "due_date": "2023-10-01", "priority": "High", "category": "Work", "completed": False},
    {"id": 2, "title": "Test Task 2", "description": "Description 2", "due_date": "2023-10-02", "priority": "Medium", "category": "Personal", "completed": True},
    {"id": 3, "title": "Test Task 3", "description": "Description 3", "due_date": "2023-10-03", "priority": "Low", "category": "School", "completed": False}
]

@pytest.fixture
def setup_tasks(tmp_path):
    test_file = tmp_path / "test_tasks.json"
    with open(test_file, "w") as f:
        json.dump(mock_tasks, f)
    return str(test_file)

def test_load_tasks(setup_tasks):
    tasks = load_tasks(setup_tasks)
    assert len(tasks) == 3
    assert tasks[0]["title"] == "Test Task 1"

def test_save_tasks(setup_tasks):
    tasks = load_tasks(setup_tasks)
    new_task = {"id": 4, "title": "Test Task 4", "description": "Description 4", "due_date": "2023-10-04", "priority": "Low", "category": "Work", "completed": False}
    tasks.append(new_task)
    save_tasks(tasks, setup_tasks)
    updated_tasks = load_tasks(setup_tasks)
    assert len(updated_tasks) == 4
    assert updated_tasks[-1]["title"] == "Test Task 4"

def test_filter_tasks_by_priority(setup_tasks):
    filtered_tasks = filter_tasks_by_priority(load_tasks(setup_tasks), "High")
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0]["title"] == "Test Task 1"

def test_filter_tasks_by_category(setup_tasks):
    filtered_tasks = filter_tasks_by_category(load_tasks(setup_tasks), "Personal")
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0]["title"] == "Test Task 2"

def test_filter_tasks_by_completion(setup_tasks):
    tasks = load_tasks(setup_tasks)
    completed_tasks = filter_tasks_by_completion(tasks, True)
    assert len(completed_tasks) == 1
    assert completed_tasks[0]["title"] == "Test Task 2"