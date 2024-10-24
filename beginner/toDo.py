import json
import os
from modules import menu, get_int
from datetime import datetime

folder_path = 'beginner/files'
file_name = "toDo.json"
file_path = os.path.join(folder_path, file_name)

def save_tasks(tasks, filename=file_path):
    try:
        # Ensure the folder exists
        os.makedirs(folder_path, exist_ok=True)
        with open(filename, "w") as f:
            json.dump(tasks, f, indent=4)
            print(f'Successfully saved tasks to {filename}')
    except Exception as e:
        print(f"Error saving tasks: {e}")
        
def load_tasks(filename=file_path):
    try:
        with open(filename, 'r') as f:
            tasks = json.load(f)
            print(f"Loaded {len(tasks)} tasks from {filename}")
            return tasks
    except FileNotFoundError:
        print("No saved tasks found. Starting with an empty to-do list.")
        return []
    except json.JSONDecodeError:
        print("Error reading the file. Starting with an empty to-do list.")
        return []

def delete_task(tasks):
    task_index = get_int("Enter task number to remove: ") - 1
    if 0 <= task_index < len(tasks):
        confirm = input(f'Are you sure you want to remove "{tasks[task_index]["task"]}"? (y/n) ')
        if confirm.lower() == 'y':
            removed_task = tasks.pop(task_index)
            print(f"Task '{removed_task['task']}' removed!")
        else:
            print("Task not removed.")
    else:
        print('Invalid task number.')

def search_tasks(tasks):
    search_term = input('Enter a keyword to search for: ').strip().lower()
    matches = [
        task for task in tasks if search_term in task["task"].lower()
    ]
    
    if matches:
        print('\nSearch Results:')
        print(f"{'No.':<5} {'Task':<40} {'Status':<10} {'Created':<20} {'Completed':<20}")
        print("-" * 95)  # A line for better readability
        for index, task in enumerate(matches):
            status = "Done" if task['done'] else "Not Done"
            created = task["created"]
            completed = task["completed"] if task["completed"] else "Not Completed"
            print(f"{index + 1:<5} {task['task']:<40} {status:<10} {created:<20} {completed:<20}")
    else:
        print("No matching results.")

def mark_done(tasks):
    task_index = get_int("Enter task number to mark as done: ") - 1
    if 0 <= task_index < len(tasks):
        if not tasks[task_index]["done"]:
            tasks[task_index]["done"] = True
            print(f"Task '{tasks[task_index]['task']}' marked as done!")
        else:
            print(f"Task '{tasks[task_index]['task']}' is already done.")
    else:
        print("Invalid task number.")

def show_tasks(tasks):
    if tasks:
        print("\nTasks")
        print(f"{'No.':<5} {'Task':<40} {'Status':<10} {'Created':<20} {'Completed':<20}")
        print("-" * 95)  # A line for better readability
        for index, task in enumerate(tasks):
            status = "Done" if task['done'] else "Not Done"
            created = task["created"]
            completed = task["completed"] if task["completed"] else "Not Completed"
            print(f"{index + 1:<5} {task['task']:<40} {status:<10} {created:<20} {completed:<20}")    
    else:
        print("\nNo tasks to show.")

def add_task(tasks):
    print()
    n_tasks = get_int("How many tasks do you want to add?")
    for i in range(n_tasks):
        task = input("Enter task: ")
        tasks.append({"task": task,
                      "done": False,
                     "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     "completed": None
                     })
        print(f"Task '{task}' added!")

def main():
    tasks = load_tasks()  # Load existing tasks if available
    
    while True:
        show_tasks(tasks)
        choice = menu(["Add Task", "Mark Task as Done", "Remove Task", "Search Tasks", "Exit"], "\n==== To-Do List ====")
        if choice == 0:
            add_task(tasks)
        elif choice == 1:
            mark_done(tasks)
        elif choice == 2:
            delete_task(tasks)
        elif choice == 3:
            search_tasks(tasks)
        elif choice == 4:
            print('Exiting the To-Do List.')
            save_tasks(tasks)  # Save tasks before exiting
            break

main()
