# 📋 To-Do List Application (Python CLI)

A clean, menu-driven, terminal-based To-Do List manager built with
**Object-Oriented Programming (OOP)** principles in Python. This project
was developed as part of the **CodSoft Python Internship** program.

---

## 📖 Project Overview

This application allows users to manage their daily tasks directly from
the command line. It supports adding, viewing, editing, deleting, and
searching tasks, along with marking them as completed and viewing
overall task statistics. All data is automatically saved to a local
JSON file, so tasks persist between sessions.

The project is intentionally structured with clear separation of
concerns:

| Class          | Responsibility                                   |
|----------------|---------------------------------------------------|
| `Task`         | Represents a single task (data model)             |
| `TaskStorage`  | Handles reading/writing tasks to `tasks.json`     |
| `TaskManager`  | Contains all core business logic (CRUD, search)   |
| `ToDoApp`      | Manages the CLI menu and user interaction         |

---

## ✨ Features

- 🟢 **Add Task** — Create a new task with an automatic timestamp.
- 📃 **View Tasks** — List all tasks with serial numbers and status.
- ✅ **Mark as Completed** — Update a task's status to completed.
- ✏️ **Edit Task** — Update the description of an existing task.
- 🗑️ **Delete Task** — Remove a task from the list.
- 🔍 **Search Tasks** — Find tasks by keyword (case-insensitive).
- 📊 **Task Statistics** — View total, completed, and pending task counts.
- 💾 **Auto-Save** — Tasks are saved to `tasks.json` after every change.
- 🔄 **Auto-Load** — Previously saved tasks load automatically on startup.
- 🛡️ **Error Handling** — Gracefully handles invalid menu choices, empty
  input, out-of-range task numbers, and corrupted data files.
- 🧩 **Modular OOP Design** — Fully separated into reusable classes and
  methods, following PEP 8 style guidelines.

---

## 🛠️ Technologies Used

- **Language:** Python 3.8+
- **Standard Library Modules:**
  - `json` — for persistent data storage
  - `os` — for file existence checks
  - `datetime` — for task creation timestamps
- **Paradigm:** Object-Oriented Programming (OOP)
- **Interface:** Command-Line Interface (CLI)

No external/third-party libraries or installations are required.

---

## ⚙️ Installation Steps

1. **Ensure Python is installed** (version 3.8 or higher):
   ```bash
   python3 --version
   ```

2. **Clone or download this project folder**:
   ```bash
   git clone <your-repository-link>
   cd ToDoList
   ```
   (Or simply copy the `ToDoList` folder to your machine.)

3. No additional dependencies need to be installed — the project uses
   only Python's built-in standard library.

---

## ▶️ How to Run

From inside the `ToDoList` folder, run:

```bash
python3 main.py
```

On Windows, you may instead use:

```bash
python main.py
```

The application will display a welcome banner followed by an
interactive menu. Simply enter the number corresponding to the action
you want to perform.

---

## 🖥️ Sample Output

```
 _____     ____        _        _     _     _
|_   _|__ |  _ \  ___ | |      | |   (_)___| |_
  | |/ _ \| | | |/ _ \| |      | |   | / __| __|
  | | (_) | |_| | (_) | |      | |___| \__ \ |_
  |_|\___/|____/ \___/|_|      |_____|_|___/\__|

        Welcome to the CLI To-Do List Application

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

👉 Enter your choice (1-8): 1
Enter the task description: Complete CodSoft internship task
✅ Task added successfully: "Complete CodSoft internship task"

👉 Enter your choice (1-8): 2

------------------------------------------------------------
#   TASK                                         STATUS
------------------------------------------------------------
1   Complete CodSoft internship task              ✘ Pending
------------------------------------------------------------

👉 Enter your choice (1-8): 7

📊 TASK STATISTICS
------------------------------
Total Tasks     : 1
Completed Tasks : 0
Pending Tasks   : 1
------------------------------

👉 Enter your choice (1-8): 8

👋 Thank you for using the To-Do List App. Goodbye!
```

---

## 🚀 Future Enhancements

- 🗓️ Add due dates and reminders for tasks.
- 🔺 Introduce task priority levels (High / Medium / Low).
- 🎨 Add color-coded terminal output using libraries like `colorama`.
- 🌐 Build a GUI version using `Tkinter` or a web version using `Flask`.
- 🔐 Add multi-user support with individual login-based task lists.
- 📤 Add export options (CSV/PDF) for task reports.
- 🔃 Add sorting options (by date, status, or alphabetically).

---

## 📁 Folder Structure

```
ToDoList/
│── main.py        # Core application source code
│── tasks.json      # Auto-generated file for persistent task storage
│── README.md       # Project documentation (this file)
```

---

## 📝 License

This project was created for educational purposes as part of the
**CodSoft Python Internship**. Free to use and modify for learning.
