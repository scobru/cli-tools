import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

def add_task(tasks, title, description, due_date):
    task = {"title": title, "description": description, "due_date": due_date, "completed": False}
    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully!")

def list_tasks(tasks):
    for index, task in enumerate(tasks, start=1):
        print(f"{index}. {task['title']} - Due: {task['due_date']} - {'Completed' if task['completed'] else 'Incomplete'}")

def update_task(tasks, index, title, description, due_date):
    if 0 < index <= len(tasks):
        task = tasks[index - 1]
        task["title"] = title
        task["description"] = description
        task["due_date"] = due_date
        save_tasks(tasks)
        print("Task updated successfully!")
    else:
        print("Invalid task index.")

# Add other functions for deleting, searching, marking as complete, etc.

def main():
    tasks = load_tasks()

    while True:
        print("\nTask Manager Menu:")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Update Task")
        print("4. Quit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            add_task(tasks, title, description, due_date)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            list_tasks(tasks)
            index = int(input("Enter the index of the task to update: "))
            title = input("Enter new task title: ")
            description = input("Enter new task description: ")
            due_date = input("Enter new due date (YYYY-MM-DD): ")
            update_task(tasks, index, title, description, due_date)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()