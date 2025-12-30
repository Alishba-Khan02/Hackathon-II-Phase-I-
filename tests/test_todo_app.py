import pytest
from src.todo_app.main import TaskManager

def test_add_task_valid():
    task_manager = TaskManager()
    task = task_manager.add_task("Test Title", "Test Description")
    assert task.id == 1
    assert task.title == "Test Title"
    assert task.description == "Test Description"
    assert not task.completed
    assert len(task_manager.get_all_tasks()) == 1

def test_add_task_unique_id():
    task_manager = TaskManager()
    task1 = task_manager.add_task("Test 1")
    task2 = task_manager.add_task("Test 2")
    assert task1.id != task2.id
    assert task2.id == task1.id + 1

def test_add_task_empty_title():
    task_manager = TaskManager()
    with pytest.raises(ValueError, match="Title cannot be empty."):
        task_manager.add_task("")

def test_get_all_tasks_empty():
    task_manager = TaskManager()
    assert task_manager.get_all_tasks() == []

def test_get_all_tasks_multiple():
    task_manager = TaskManager()
    task1 = task_manager.add_task("Test 1")
    task2 = task_manager.add_task("Test 2")
    task2.completed = True
    tasks = task_manager.get_all_tasks()
    assert len(tasks) == 2
    assert tasks[0] == task1
    assert tasks[1] == task2

def test_update_task_valid():
    task_manager = TaskManager()
    task = task_manager.add_task("Test Title")
    updated_task = task_manager.update_task(task.id, "New Title", "New Description")
    assert updated_task.title == "New Title"
    assert updated_task.description == "New Description"
    assert task.title == "New Title"
    assert task.description == "New Description"

def test_update_task_invalid_id():
    task_manager = TaskManager()
    task_manager.add_task("Test Title")
    updated_task = task_manager.update_task(999, "New Title")
    assert updated_task is None

def test_delete_task_valid():
    task_manager = TaskManager()
    task = task_manager.add_task("Test Title")
    assert len(task_manager.get_all_tasks()) == 1
    deleted = task_manager.delete_task(task.id)
    assert deleted is True
    assert len(task_manager.get_all_tasks()) == 0

def test_delete_task_invalid_id():
    task_manager = TaskManager()
    task_manager.add_task("Test Title")
    deleted = task_manager.delete_task(999)
    assert deleted is False
    assert len(task_manager.get_all_tasks()) == 1

def test_toggle_task_status_valid():
    task_manager = TaskManager()
    task = task_manager.add_task("Test Title")
    assert not task.completed
    updated_task = task_manager.toggle_task_status(task.id)
    assert updated_task.completed
    updated_task = task_manager.toggle_task_status(task.id)
    assert not updated_task.completed

from src.todo_app.main import main
def test_toggle_task_status_invalid_id():
    task_manager = TaskManager()
    task_manager.add_task("Test Title")
    updated_task = task_manager.toggle_task_status(999)
    assert updated_task is None

def test_main_menu_exit(capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '6')
    main()
    captured = capsys.readouterr()
    assert "--- Todo App Menu ---" in captured.out
    assert "Exiting Todo App." in captured.out

def test_main_menu_invalid_choice(capsys, monkeypatch):
    # Simulate invalid choice then exit
    inputs = iter(['9', '6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main()
    captured = capsys.readouterr()
    assert "Invalid choice. Please try again." in captured.out

