import streamlit as st
import pandas as pd
import subprocess
from datetime import datetime
from tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category, generate_unique_id, search_tasks, get_overdue_tasks

def main():
    st.title("Stephen's To-Do Application")
    
    # Load existing tasks
    tasks = load_tasks()
    
    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")
    
    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")
        
        if submit_button and task_title:
            new_task = {
                "id": generate_unique_id(tasks),
                "title": task_title,
                "description": task_description,
                "priority": task_priority,
                "category": task_category,
                "due_date": task_due_date.strftime("%Y-%m-%d"),
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            tasks.append(new_task)
            save_tasks(tasks)
            st.sidebar.success("Task added successfully!")
    
    #I DID: IMPLEMENT SEARCH FUNCTIONALITY
    search_query = st.text_input("Search Tasks")

    # Main area to display tasks
    st.header("Your Tasks")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(set([task["category"] for task in tasks])))
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    
    show_completed = st.checkbox("Show Completed Tasks")
    
    show_overdue = st.sidebar.checkbox("Show Overdue Tasks")

    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
    
    if search_query:
        filtered_tasks = search_tasks(filtered_tasks, search_query)

    if show_overdue:
        overdue_tasks = get_overdue_tasks(filtered_tasks)
        filtered_tasks.extend(overdue_tasks)

    # Display tasks
    for task in filtered_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
            else:
                st.markdown(f"**{task['title']}**")
            st.write(task["description"])
            st.caption(f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}")
        with col2:
            if st.button("Complete" if not task["completed"] else "Undo", key=f"complete_{task['id']}"):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        try:
                            save_tasks(tasks)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error saving task: {e}")
                            return
            if st.button("Edit", key=f"edit_{task['id']}"):
                with st.form(f"edit_task_form_{task['id']}"):
                    # Pre-populate the form with task data
                    task_title = st.text_input("Task Title", task["title"])
                    task_description = st.text_area("Description", task["description"])
                    task_priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(task["priority"]))
                    task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"], index=["Work", "Personal", "School", "Other"].index(task["category"]))
                    task_due_date = st.date_input("Due Date", pd.to_datetime(task["due_date"]).date())
                    
                    submit_button = st.form_submit_button("Update Task")
                    if submit_button:
                        # Update task with new values
                        task["title"] = task_title
                        task["description"] = task_description
                        task["priority"] = task_priority
                        task["category"] = task_category
                        task["due_date"] = task_due_date.strftime("%Y-%m-%d")
                        try:
                            save_tasks(tasks)  # Save updated task
                            st.success("Task updated successfully!")
                            st.rerun()  # Rerun the app to reflect changes
                        except Exception as e:
                            st.error(f"Error saving task: {e}")
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()

    st.markdown("---")
    st.header("TESTING")

    if st.button("Run Unit Tests"):
        with st.spinner("Running tests..."):
            result = subprocess.run(["pytest", "tests/test_basic.py", "--disable-warnings"], capture_output=True, text=True)
            st.code(result.stdout, language="python")

    st.markdown("---")
    st.header("PYTEST FEATURES")

    def run_pytest_coverage():
        result = subprocess.run(["pytest", "--cov=tasks", "--cov-report=term-missing"], capture_output=True, text=True)
        st.text(result.stdout)

    def run_pytest_parametrize():
        result = subprocess.run(["pytest", "-k", "test_task_priority"], capture_output=True, text=True)
        st.text(result.stdout)

    def run_pytest_mock():
        result = subprocess.run(["pytest", "-m", "mock"], capture_output=True, text=True)
        st.text(result.stdout)

    def run_pytest_html_report():
        result = subprocess.run([
            "pytest", 
            "--html=report.html", 
            "--self-contained-html"
        ], capture_output=True, text=True)
        st.text(result.stdout)

    def run_tdd_tests():
        result = subprocess.run(["pytest", "tests/test_tdd.py"], capture_output=True, text=True)
        st.text(result.stdout)

    def run_bdd_tests():
        result = subprocess.run(["pytest", "tests/test_bdd.py"], capture_output=True, text=True)
        st.text(result.stdout)

    def run_property_based_tests():
        result = subprocess.run(["pytest", "tests/test_property.py", "--hypothesis-show-statistics"], capture_output=True, text=True)
        st.text(result.stdout)

    if st.button('Run Coverage Report'):
        run_pytest_coverage()

    if st.button('Run Parameterized Tests'):
        run_pytest_parametrize()

    if st.button('Run Mocking Tests'):
        run_pytest_mock()

    if st.button('Run HTML Report'):
        run_pytest_html_report()

    st.markdown("---")
    st.header("TDD TESTS")

    if st.button("Run TDD Tests"):
        run_tdd_tests()

    st.markdown("---")
    st.header("BDD TESTS")

    if st.button("Run BDD Tests"):
        run_bdd_tests()

    st.markdown("---")
    st.header("HYPOTHESIS TESTS")
    if st.button("Run Property-Based Tests"):
        run_property_based_tests()
    


if __name__ == "__main__":
    main()