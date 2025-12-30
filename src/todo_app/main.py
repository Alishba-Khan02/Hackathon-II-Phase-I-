from typing import List, Optional
from .models import Task

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        if not title:
            raise ValueError("Title cannot be empty.")
        task = Task(id=self.next_id, title=title, description=description)
        self.tasks.append(task)
        self.next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        return self.tasks

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: str, description: Optional[str] = None) -> Optional[Task]:
        task = self.get_task_by_id(task_id)
        if task:
            if title:
                task.title = title
            if description:
                task.description = description
            return task
        return None

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def toggle_task_status(self, task_id: int) -> Optional[Task]:
        task = self.get_task_by_id(task_id)
        if task:
            task.completed = not task.completed
            return task
        return None

def display_tasks(tasks: List[Task]):
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        status = "✓" if task.completed else "✗"
        print(f"[{status}] ID: {task.id}, Title: {task.title}, Description: {task.description}")

def main():
    task_manager = TaskManager()

    while True:
        print("\n--- Todo App Menu ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task as Complete/Incomplete")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description (optional): ")
            try:
                task = task_manager.add_task(title, description)
                print(f"Task '{task.title}' added with ID: {task.id}")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '2':
            tasks = task_manager.get_all_tasks()
            display_tasks(tasks)
        elif choice == '3':
            try:
                task_id = int(input("Enter task ID to update: "))
                title = input("Enter new title (optional): ")
                description = input("Enter new description (optional): ")
                task = task_manager.update_task(task_id, title, description)
                if task:
                    print(f"Task {task_id} updated.")
                else:
                    print(f"Task with ID {task_id} not found.")
            except ValueError:
                print("Invalid input. Please enter a number for the task ID.")
        elif choice == '4':
            try:
                task_id = int(input("Enter task ID to delete: "))
                if task_manager.delete_task(task_id):
                    print(f"Task {task_id} deleted.")
                else:
                    print(f"Task with ID {task_id} not found.")
            except ValueError:
                print("Invalid input. Please enter a number for the task ID.")
        elif choice == '5':
            try:
                task_id = int(input("Enter task ID to toggle status: "))
                task = task_manager.toggle_task_status(task_id)
                if task:
                    status = "complete" if task.completed else "incomplete"
                    print(f"Task {task_id} marked as {status}.")
                else:
                    print(f"Task with ID {task_id} not found.")
            except ValueError:
                print("Invalid input. Please enter a number for the task ID.")
        elif choice == '6':
            print("Exiting Todo App.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
