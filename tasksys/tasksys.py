#!/usr/bin/env python3
#Version = 1.0.0
'''
TaskSys — Minimal Task Manager Popup for Rofi
---------------------------------------------
Usage:
  tasksys.py [options]

Keyboard Shortcuts (inside Rofi View):
  alt+enter  = Add task
  shift+enter = Delete task
  enter      = Toggle Done
  esc        = Exit

Description:
  TaskSys is a keyboard-driven task manager integrated with Rofi.
  Use it to quickly add, view, and mark tasks as done without leaving your workflow.
'''
#Dont forget to make the python file executable
import json
import subprocess
from pathlib import Path

TASKS_FILE = Path.home() / ".local/share/tasksys/tasks.json"

#Make sure folder exists
TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_tasks():
    if TASKS_FILE.exists():
        with open(TASKS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def rofi_menu(options, prompt="Tasks", message=None, kb_custom=None):
    """
    Display a Rofi menu and return the user's selected item and keycode.
    """
    cmd = [
        "rofi", "-dmenu", "-i", "-p", prompt,
        "-kb-custom-1", "Alt+Return",
        "-kb-custom-2", "Alt+Delete"
    ]
    if message:
        cmd += ["-mesg", message]
    result = subprocess.run(
        cmd,
        input="\n".join(options),
        text=True,
        capture_output=True
    )
    return result.stdout.strip(), result.returncode

def add_task():
    name = subprocess.run(
        ["rofi", "-dmenu", "-p", "Enter new task name:"],
        text=True,
        capture_output=True
    ).stdout.strip()
    if not name:
        return
    tasks = load_tasks()
    tasks.append({"name": name, "done": False})
    save_tasks(tasks)

def toggle_task(selected_name):
    tasks = load_tasks()
    for t in tasks:
        if f"[{'x' if t['done'] else ' '}] {t['name']}" == selected_name:
            t["done"] = not t["done"]
            break
    save_tasks(tasks)

def delete_task(selected_name):
    tasks = load_tasks()
    tasks = [t for t in tasks if f"[{'x' if t['done'] else ' '}] {t['name']}" != selected_name]
    save_tasks(tasks)

def view_tasks():
    while True:
        tasks = load_tasks()
        msg = "alt+enter = Add task     alt+delete = Delete task\nenter = Toggle Done     esc = Exit"
        options = [f"[{'x' if t['done'] else ' '}] {t['name']}" for t in tasks] or ["(No tasks)"]
        choice, code = rofi_menu(
            options,
            prompt="tasksys",
            message=msg
        )

        # Exit
        if code == 1 or not choice:
            break
        # Alt+Enter → Add Task
        elif code == 10:
            add_task()
        # Shift+Enter → Delete Task
        elif code == 11 and choice != "(No tasks)":
            delete_task(choice)
        # Enter → Toggle Done
        elif code == 0 and choice != "(No tasks)":
            toggle_task(choice)

def waybar_output():
    tasks = load_tasks()
    total = len(tasks)
    done = len([t for t in tasks if t["done"]])
    pending = total - done
    output = {
        "text": f" {pending}/{total}",
        "tooltip": f"{pending} Pending / {total} Total" if total > 0 else "No tasks yet.",
        "class": "tasksyson" if pending > 0 else "tasksysoff"
    }
    print(json.dumps(output))

if __name__ == "__main__":
    import sys
    if "--popup" in sys.argv:
        view_tasks()
    else:
        waybar_output()
