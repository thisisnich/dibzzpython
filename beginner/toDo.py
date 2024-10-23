import json
import os
from modules import menu, get_int

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
        confirm = input(f'Are you sure you want to remove {tasks[task_index]['task']}? (y/n)')
        if confirm == 'y':
            removed_task = tasks.pop(task_index)
            print(f"Task {removed_task['task']} removed!")
        else:
            print("Task not removed.")
    else:
        print('invalid task number.')

def search_tasks(tasks):
    searchTearm = input('Enter a keyword to search for: ').strip().lower()
    matches = [
        task for task in tasks if searchTearm in task["task"].lower()
    ]
    
    if matches:
        print('\nSearch Results: ')
        for index, task in enumerate(matches):
            status = "Done" if task['done'] else "Not Done"
            print(f'{index+1}. {task["task"]} - {status}')
    else:
        print("No matching results")

def main():
    tasks = load_tasks()  # Load existing tasks if available
    
    while True:
        choice = menu(["Add Task", "Show Tasks", "Mark Task as Done","Remove Task", "Search Tasks", "Exit"], "\n==== To-Do List ====")
        if choice == 0:
            print()
            n_tasks = get_int("How many tasks do you want to add?")
            for i in range(n_tasks):
                task = input("Enter task: ")
                tasks.append({"task": task, "done": False})
                print(f"Task '{task}' added!")
        
        elif choice == 1:
            if tasks:
                print("\nTasks")
                for index, task in enumerate(tasks):
                    status = "Done" if task["done"] else "Not Done"
                    print(f'{index + 1}. {task["task"]} - {status}')
            else:
                print("\nNo tasks to show.")
        
        elif choice == 2:
            task_index = get_int("Enter task number to mark as done: ") - 1
            if 0 <= task_index < len(tasks):
                if not tasks[task_index]["done"]:
                    tasks[task_index]["done"] = True
                    print(f"Task '{tasks[task_index]['task']}' marked as done!")
                else:
                    print(f"Task '{tasks[task_index]['task']}' is already done.")
            else:
                print("Invalid task number.")
        elif choice == 3:
            delete_task(tasks)
        
        elif choice == 4:
            search_tasks(tasks)
        
        elif choice == 5:
            print('Exiting the To-Do List.')
            save_tasks(tasks)  # Save tasks before exiting
            break

main()
