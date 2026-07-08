#!/usr/bin/env python3
"""
To-Do List Application (CLI)
=============================

A menu-driven, terminal-based To-Do List manager built using
Object-Oriented Programming principles.

Author : Senior Python Engineer
Project: CodSoft Python Internship - Task 1 (To-Do List Application)

Features:
    - Add, view, edit, delete, and search tasks
    - Mark tasks as completed
    - View task statistics (Total, Completed, Pending)
    - Persistent storage using a JSON file
    - Automatic loading of saved tasks on startup
    - Robust exception handling for invalid input

This module is intentionally kept in a single file for simplicity of
submission, but functionality is cleanly separated into classes and
methods so it can easily be split into multiple modules if required.
"""

import json
import os
from datetime import datetime


# --------------------------------------------------------------------------- #
#  DATA MODEL
# --------------------------------------------------------------------------- #
class Task:
    """
    Represents a single To-Do task.

    Attributes:
        title (str): The description/title of the task.
        completed (bool): Whether the task has been completed.
        created_at (str): Timestamp when the task was created.
    """

    def __init__(self, title: str, completed: bool = False, created_at: str = None):
        self.title = title
        self.completed = completed
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def mark_completed(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def update_title(self, new_title: str) -> None:
        """Update the task's title/description."""
        self.title = new_title

    def to_dict(self) -> dict:
        """Convert the Task object into a dictionary (for JSON storage)."""
        return {
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        """Create a Task object from a dictionary (loaded from JSON)."""
        return Task(
            title=data.get("title", "Untitled Task"),
            completed=data.get("completed", False),
            created_at=data.get("created_at"),
        )

    def __str__(self) -> str:
        status = "✔ Completed" if self.completed else "✘ Pending"
        return f"{self.title}  [{status}]  (Added: {self.created_at})"


# --------------------------------------------------------------------------- #
#  STORAGE HANDLER
# --------------------------------------------------------------------------- #
class TaskStorage:
    """
    Handles reading and writing tasks to a JSON file.
    Keeps persistence logic separate from business logic (Single
    Responsibility Principle).
    """

    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = file_path

    def load_tasks(self) -> list:
        """
        Load tasks from the JSON file.

        Returns:
            list: A list of Task objects. Returns an empty list if the
                  file does not exist or contains invalid/corrupted data.
        """
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                raw_data = json.load(file)
                return [Task.from_dict(item) for item in raw_data]
        except (json.JSONDecodeError, ValueError):
            print("⚠  Warning: tasks.json is corrupted or unreadable. "
                  "Starting with an empty task list.")
            return []
        except OSError as error:
            print(f"⚠  Warning: Could not read task file ({error}). "
                  "Starting with an empty task list.")
            return []

    def save_tasks(self, tasks: list) -> None:
        """
        Save the given list of Task objects to the JSON file.

        Args:
            tasks (list): List of Task objects to persist.
        """
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([task.to_dict() for task in tasks], file, indent=4)
        except OSError as error:
            print(f"❌ Error: Could not save tasks to file ({error}).")


# --------------------------------------------------------------------------- #
#  BUSINESS LOGIC / TASK MANAGER
# --------------------------------------------------------------------------- #
class TaskManager:
    """
    Core manager class that contains all business logic for
    manipulating the task list: add, view, edit, delete, search,
    mark complete, and generate statistics.
    """

    def __init__(self, storage: TaskStorage):
        self.storage = storage
        self.tasks = self.storage.load_tasks()

    # ---------------------- Persistence Helper ---------------------- #
    def _save(self) -> None:
        """Persist current task list to storage (internal helper)."""
        self.storage.save_tasks(self.tasks)

    # ---------------------------- Add -------------------------------- #
    def add_task(self, title: str) -> None:
        """Add a new task to the list and save it."""
        title = title.strip()
        if not title:
            raise ValueError("Task description cannot be empty.")

        new_task = Task(title)
        self.tasks.append(new_task)
        self._save()
        print(f"✅ Task added successfully: \"{title}\"")

    # ---------------------------- View -------------------------------- #
    def view_tasks(self) -> None:
        """Display all tasks with serial numbers."""
        if not self.tasks:
            print("📭 No tasks found. Your to-do list is empty!")
            return

        print("\n" + "-" * 60)
        print(f"{'#':<4}{'TASK':<45}{'STATUS'}")
        print("-" * 60)
        for index, task in enumerate(self.tasks, start=1):
            status = "✔ Completed" if task.completed else "✘ Pending"
            print(f"{index:<4}{task.title:<45}{status}")
        print("-" * 60 + "\n")

    # ------------------------ Mark Completed --------------------------- #
    def mark_completed(self, index: int) -> None:
        """
        Mark the task at the given 1-based index as completed.

        Raises:
            IndexError: If the index is out of the valid range.
        """
        self._validate_index(index)
        task = self.tasks[index - 1]

        if task.completed:
            print(f"ℹ️  Task \"{task.title}\" is already marked as completed.")
            return

        task.mark_completed()
        self._save()
        print(f"✅ Task marked as completed: \"{task.title}\"")

    # ---------------------------- Edit -------------------------------- #
    def edit_task(self, index: int, new_title: str) -> None:
        """
        Edit/update the title of the task at the given 1-based index.

        Raises:
            IndexError: If the index is out of range.
            ValueError: If the new title is empty.
        """
        self._validate_index(index)
        new_title = new_title.strip()
        if not new_title:
            raise ValueError("Updated task description cannot be empty.")

        old_title = self.tasks[index - 1].title
        self.tasks[index - 1].update_title(new_title)
        self._save()
        print(f"✏️  Task updated: \"{old_title}\" → \"{new_title}\"")

    # --------------------------- Delete -------------------------------- #
    def delete_task(self, index: int) -> None:
        """
        Delete the task at the given 1-based index.

        Raises:
            IndexError: If the index is out of range.
        """
        self._validate_index(index)
        removed_task = self.tasks.pop(index - 1)
        self._save()
        print(f"🗑️  Task deleted: \"{removed_task.title}\"")

    # --------------------------- Search -------------------------------- #
    def search_tasks(self, keyword: str) -> None:
        """Search and display tasks whose title contains the keyword."""
        keyword = keyword.strip().lower()
        if not keyword:
            raise ValueError("Search keyword cannot be empty.")

        results = [
            (i, task) for i, task in enumerate(self.tasks, start=1)
            if keyword in task.title.lower()
        ]

        if not results:
            print(f"🔍 No tasks found matching keyword: \"{keyword}\"")
            return

        print(f"\n🔍 Found {len(results)} matching task(s):")
        print("-" * 60)
        for index, task in results:
            status = "✔ Completed" if task.completed else "✘ Pending"
            print(f"{index:<4}{task.title:<45}{status}")
        print("-" * 60 + "\n")

    # -------------------------- Statistics -------------------------------- #
    def show_statistics(self) -> None:
        """Display total, completed, and pending task counts."""
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task.completed)
        pending = total - completed

        print("\n📊 TASK STATISTICS")
        print("-" * 30)
        print(f"Total Tasks     : {total}")
        print(f"Completed Tasks : {completed}")
        print(f"Pending Tasks   : {pending}")
        print("-" * 30 + "\n")

    # --------------------------- Validation -------------------------------- #
    def _validate_index(self, index: int) -> None:
        """Ensure the given 1-based index refers to an existing task."""
        if not self.tasks:
            raise IndexError("There are no tasks available.")
        if index < 1 or index > len(self.tasks):
            raise IndexError(
                f"Invalid task number. Please enter a number between "
                f"1 and {len(self.tasks)}."
            )


# --------------------------------------------------------------------------- #
#  USER INTERFACE (CLI)
# --------------------------------------------------------------------------- #
class ToDoApp:
    """
    Handles the command-line user interface: displaying menus,
    collecting user input, and dispatching actions to the TaskManager.
    """

    MENU_OPTIONS = """
╔══════════════════════════════════════════════╗
║               📋  MAIN MENU  📋                ║
╠══════════════════════════════════════════════╣
║ 1. Add a new task                             ║
║ 2. View all tasks                             ║
║ 3. Mark a task as completed                   ║
║ 4. Edit/update a task                         ║
║ 5. Delete a task                              ║
║ 6. Search tasks by keyword                    ║
║ 7. View task statistics                       ║
║ 8. Exit                                       ║
╚══════════════════════════════════════════════╝
"""

    def __init__(self):
        self.manager = TaskManager(TaskStorage("tasks.json"))

    # --------------------------- Banner -------------------------------- #
    @staticmethod
    def display_banner() -> None:
        """Print the welcome banner shown at application startup."""
        banner = r"""
 _____     ____        _        _     _     _
|_   _|__ |  _ \  ___ | |      | |   (_)___| |_
  | |/ _ \| | | |/ _ \| |      | |   | / __| __|
  | | (_) | |_| | (_) | |      | |___| \__ \ |_
  |_|\___/|____/ \___/|_|      |_____|_|___/\__|

        Welcome to the CLI To-Do List Application
"""
        print(banner)

    # ---------------------------- Runner -------------------------------- #
    def run(self) -> None:
        """Main application loop. Keeps running until the user exits."""
        self.display_banner()

        while True:
            print(self.MENU_OPTIONS)
            choice = input("👉 Enter your choice (1-8): ").strip()

            try:
                if choice == "1":
                    self._handle_add_task()
                elif choice == "2":
                    self.manager.view_tasks()
                elif choice == "3":
                    self._handle_mark_completed()
                elif choice == "4":
                    self._handle_edit_task()
                elif choice == "5":
                    self._handle_delete_task()
                elif choice == "6":
                    self._handle_search_tasks()
                elif choice == "7":
                    self.manager.show_statistics()
                elif choice == "8":
                    print("\n👋 Thank you for using the To-Do List App. Goodbye!\n")
                    break
                else:
                    print("❌ Invalid choice. Please select a number between 1 and 8.")

            except ValueError as error:
                print(f"❌ Error: {error}")
            except IndexError as error:
                print(f"❌ Error: {error}")
            except Exception as error:  # Fallback for any unexpected issues
                print(f"❌ An unexpected error occurred: {error}")

    # ---------------------- Input Handlers ---------------------- #
    def _handle_add_task(self) -> None:
        title = input("Enter the task description: ")
        self.manager.add_task(title)

    def _handle_mark_completed(self) -> None:
        self.manager.view_tasks()
        index = self._read_task_index("Enter the task number to mark as completed: ")
        self.manager.mark_completed(index)

    def _handle_edit_task(self) -> None:
        self.manager.view_tasks()
        index = self._read_task_index("Enter the task number to edit: ")
        new_title = input("Enter the updated task description: ")
        self.manager.edit_task(index, new_title)

    def _handle_delete_task(self) -> None:
        self.manager.view_tasks()
        index = self._read_task_index("Enter the task number to delete: ")
        self.manager.delete_task(index)

    def _handle_search_tasks(self) -> None:
        keyword = input("Enter a keyword to search for: ")
        self.manager.search_tasks(keyword)

    @staticmethod
    def _read_task_index(prompt: str) -> int:
        """
        Safely read an integer task index from user input.

        Raises:
            ValueError: If the input is not a valid integer.
        """
        user_input = input(prompt).strip()
        if not user_input.isdigit():
            raise ValueError("Task number must be a positive integer.")
        return int(user_input)


# --------------------------------------------------------------------------- #
#  ENTRY POINT
# --------------------------------------------------------------------------- #
def main() -> None:
    """Application entry point."""
    app = ToDoApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted by user. Goodbye!\n")


if __name__ == "__main__":
    main()