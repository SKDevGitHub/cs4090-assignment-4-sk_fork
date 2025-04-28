import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from tasks import generate_unique_id, filter_tasks_by_priority, filter_tasks_by_completion
from hypothesis import given
import hypothesis.strategies as st

@given(st.lists(
    st.fixed_dictionaries({"id": st.integers(min_value=1)}),
    max_size=50
))
def test_generate_unique_id_property(tasks):
    new_id = generate_unique_id(tasks)
    existing_ids = [task["id"] for task in tasks]
    assert new_id not in existing_ids
    assert new_id > 0


@given(st.lists(st.dictionaries(keys=st.just("priority"), values=st.sampled_from(["High", "Medium", "Low"]))))
def test_filter_tasks_by_priority_property(tasks):
    result = filter_tasks_by_priority(tasks, "High")
    for task in result:
        assert task["priority"] == "High"

@given(st.lists(st.dictionaries(keys=st.just("completed"), values=st.booleans())))
def test_filter_tasks_by_completion_property(tasks):
    result_true = filter_tasks_by_completion(tasks, True)
    for task in result_true:
        assert task["completed"] is True

@given(st.lists(st.dictionaries(keys=st.just("completed"), values=st.booleans())))
def test_filter_tasks_by_completion_false_property(tasks):
    result_false = filter_tasks_by_completion(tasks, False)
    for task in result_false:
        assert task["completed"] is False

@given(st.text(), st.text(), st.text(), st.text(), st.booleans())
def test_task_creation_property(title, priority, category, due_date, completed):
    task = {
        "title": title,
        "priority": priority,
        "category": category,
        "due_date": due_date,
        "completed": completed
    }
    assert isinstance(task["title"], str)
    assert isinstance(task["priority"], str)
    assert isinstance(task["category"], str)
    assert isinstance(task["due_date"], str)
    assert isinstance(task["completed"], bool)
