import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from tasks import mark_task_as_important, count_completed_tasks, clear_completed_tasks

def test_mark_task_as_important():
    task = {"id": 1, "title": "Task 1", "important": False}
    updated_task = mark_task_as_important(task)
    assert updated_task["important"] is True

def test_count_completed_tasks():
    tasks = [
        {"id": 1, "completed": True},
        {"id": 2, "completed": False},
        {"id": 3, "completed": True}
    ]
    assert count_completed_tasks(tasks) == 2

def test_clear_completed_tasks():
    tasks = [
        {"id": 1, "completed": True},
        {"id": 2, "completed": False},
        {"id": 3, "completed": True}
    ]
    remaining_tasks = clear_completed_tasks(tasks)
    assert len(remaining_tasks) == 1
    assert all(not task["completed"] for task in remaining_tasks)