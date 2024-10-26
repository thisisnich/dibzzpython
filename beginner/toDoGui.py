import customtkinter as ctk
from tkinter import colorchooser, simpledialog
from datetime import datetime
import json
import os
# Initialize the CustomTkinter App
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class ToDoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.list_path = os.path.join('beginner','files','toDoGui.json')
        self.category_path = os.path.join('beginner','files','category.json')
        self.config_path = os.path.join('beginner','files','config.json')
        self.session_config = self.load_config()
        print(self.session_config)
        self.selected_tasks = set()  # Use a set to track selected task indices
        self.search_query = ""  # Initialize search_query here
        # print(self.category_path)
        # print(self.list_path)
        self.categories = self.load_categories()
        self.sorting_preference = self.session_config.get('sorting_preference') # Default sorting preference
        self.default_priority = self.session_config.get("priority")
        self.default_category = self.session_config.get("category")
        self.filter_value = self.session_config.get("filter_value")              
        self.window_size = self.session_config.get("window_size")
        
        # Window setup
        self.title("To-Do List Application")
        self.geometry("800x600")
        # List of tasks (in-memory)
        self.tasks = self.load_tasks()

        # Create UI components
        self.create_widgets()

    def create_widgets(self):
        # Task entry frame
        self.task_frame = ctk.CTkFrame(self)
        self.task_frame.pack(pady=10, padx=10, fill="x")
        #Filter Frame
        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.pack(pady=10, padx=10,fill="x")
        
        # Task List Display
        self.task_list_frame = ctk.CTkScrollableFrame(self, width=750, height=400)
        self.task_list_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Control buttons frame
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(pady=10,padx=10, fill="x")
        
        #task widgets
        self.task_entry = ctk.CTkEntry(self.task_frame, width=200, placeholder_text="Enter a new task...")
        self.task_entry.pack(side="left", padx=10)
        self.task_entry.bind("<Return>", self.on_enter_key)
        
        self.add_task_button = ctk.CTkButton(self.task_frame, text="Add Task", command=self.add_task, width=150)
        self.add_task_button.pack(side="left", padx=10)
        
        self.priority_var = ctk.StringVar(value=self.default_priority)
        self.priority_menu = ctk.CTkOptionMenu(self.task_frame, variable=self.priority_var, values=["High", "Medium", "Low"], width=150, command=self.save_config)
        self.priority_menu.pack(side="left", padx=10)
        self.category_var = ctk.StringVar(value=self.default_category)
        # print(self.category_var.get())
        self.category_menu = ctk.CTkOptionMenu(self.task_frame, variable=self.category_var,values=list(self.categories.keys()), command=self.save_config)
        self.category_menu.pack(side="left", padx=10)
        self.category_button = ctk.CTkButton(self.task_frame, text="Add Category", command=self.add_category)
        self.category_button.pack(side='left',padx=10)
        
        #Filter widgets
        self.search_entry = ctk.CTkEntry(self.filter_frame, width=200, placeholder_text="Search tasks...")
        self.search_entry.pack(side = "left", padx=10)
        self.search_entry.bind("<KeyRelease>", self.on_search)  # Bind search bar to filter tasks as you type
        
        self.filter_var = ctk.StringVar(value=self.filter_value)
        self.filter_menu = ctk.CTkOptionMenu(self.filter_frame, variable=self.filter_var, values=["All", "Active", "Completed"], command=self.filter_tasks, width=150)
        self.filter_menu.pack(side='left', padx=10)
        self.sort_var = ctk.StringVar(value=self.sorting_preference)
        self.sort_menu = ctk.CTkOptionMenu(self.filter_frame, variable=self.sort_var, values=["Creation Date", "Completion Status", "Task Name", "Priority", "Category"], command=self.sort_tasks, width=150)
        self.sort_menu.pack(side="left", padx=10)
    
        
        #control Widgets
        self.mark_done_button = ctk.CTkButton(self.control_frame, text="Mark Selected as Done", command=self.mark_selected_done)
        self.mark_done_button.pack(side="left", padx=10)

        self.mark_undone_button = ctk.CTkButton(self.control_frame,text="Mark Selected as not Done", command=self.mark_selected_undone)
        self.mark_undone_button.pack(side='left', padx=10)

        self.delete_task_button = ctk.CTkButton(self.control_frame, text="Remove Selected Tasks", command=self.delete_selected_tasks)
        self.delete_task_button.pack(side="left", padx=10)
        
        

        
        self.update_task_list()
    
    def on_search(self, event=None):
        # Update the search query based on the user's input
        self.search_query = self.search_entry.get().strip().lower()
        self.update_task_list()  # Refresh the task list based on the search query

    def add_task(self):
        task_text = self.task_entry.get()
        priority = self.priority_var.get()  # Get the selected priority
        category = self.category_var.get()
        if task_text:
            new_task = {
                "task": task_text,
                "done": False,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "completed": None,
                "priority": priority,  # Include the selected priority
                "category": category
            }
            self.tasks.append(new_task)
            self.save_tasks()
            self.task_entry.delete(0, 'end')
            self.update_task_list()


    def update_task_list(self):
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        # Clear the existing task frames
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()

        # Get the current filter setting
        filter_value = self.filter_var.get()

        # Determine which tasks should be displayed based on the filter
        if filter_value == "Active":
            filtered_tasks = [(i, task) for i, task in enumerate(self.tasks) if not task['done']]
        elif filter_value == "Completed":
            filtered_tasks = [(i, task) for i, task in enumerate(self.tasks) if task['done']]
        else:
            filtered_tasks = [(i, task) for i, task in enumerate(self.tasks)]
        if self.search_query:
            filtered_tasks = [(i, task) for i, task in filtered_tasks if self.search_query in task['task'].lower()]
        # Sort tasks based on the user's preference
        sort_options = {
            "Creation Date": lambda x: x[1]["created"],
            "Completion Status": lambda x: (x[1]["done"], x[1]["completed"] if x[1]["completed"] else ""),
            "Task Name": lambda x: x[1]["task"].lower(),
            "Priority": lambda x: (priority_order[x[1].get("priority", "Medium")], x[1]["task"].lower()),
            "Category": lambda x: x[1].get("category", "Uncategorized"),  # Sorting by category
        }

        # Get the appropriate sorting function based on user selection
        sort_key = sort_options.get(self.sort_var.get(), lambda x: x[1]["created"])
        filtered_tasks.sort(key=sort_key)
        if self.sort_var.get() == "Category":
            current_category = None
            for index, task in filtered_tasks:
                if task['category'] != current_category:
                    current_category = task['category']
                    self.create_category_header(current_category)
                self.create_task_widget(task, index, task['category'])
        # Create a widget for each filtered task
        else:
            for index, task in filtered_tasks:
                self.create_task_widget(task, index, task['category'])
        self.save_config()


    def create_task_widget(self, task, index, category):
        # Create a frame for each task
        task_frame = ctk.CTkFrame(self.task_list_frame, height=40)
        task_frame.pack(pady=5, padx=5, fill="x")

        priority_colors = {"High": "#FF6666", "Medium": "#FFDD57", "Low": "#9AD98D"}
        priority_color = priority_colors.get(task['priority'], "#2E2E2E")
        category_colors=self.load_categories()
        cat_colour=category_colors.get(category, "#2E2E2E")


        category_bar = ctk.CTkFrame(task_frame, width=10, fg_color=cat_colour,height=30)
        category_bar.grid(row=0, column = 0, sticky= 'e')# Run the application

        # Checkbox for selection
        checkbox = ctk.CTkCheckBox(
            task_frame, 
            text="",
            command=lambda idx=index: self.toggle_selection(idx),
            onvalue=True, 
            offvalue=False,
            width=0,
            border_width=2
        )
        checkbox.grid(row=0, column=1, sticky='e', padx=(0, 0), pady=(0, 0))

        # Set checkbox state if already selected
        if index in self.selected_tasks:
            checkbox.select()
        else:
            checkbox.deselect()

        # Task details
        status = "Done" if task["done"] else "Not Done"
        created = task["created"]
        completed = task["completed"] if task["completed"] else "Not Completed"

        task_info = f"{task['task']} | Status: {status} | Priority: {task['priority']} | Created: {created} | Completed: {completed}"
        task_label = ctk.CTkLabel(task_frame, text=task_info, anchor="w", text_color="green" if task["done"] else "black", height=7)
        task_label.grid(row=0, column=2, sticky='w')

        # Edit button, in a separate column to push it to the right
        edit_button = ctk.CTkButton(task_frame, text="Edit", width=30, command=lambda idx=index: self.edit_task(idx))
        edit_button.grid(row=0, column=4, padx=(5, 0), sticky='e')  # Make sure this button is aligned to the right

        # Add a spacer column to move the button to the right
        task_frame.grid_columnconfigure(4, weight=1)  # This will create space in column 3

        # Highlight if selected
        if index in self.selected_tasks:
            task_frame.configure(fg_color="#3E8E7E", border_width=1, border_color=priority_color)  # Different background color for selected tasks
            task_label.configure(text_color='black')
        else:
            if task['done']:
                task_frame.configure(fg_color="#2E2E2E", border_width=1, border_color=priority_color)  # Default color for non-selected tasks
            else:
                task_frame.configure(fg_color=priority_color)
    def edit_task(self,index):
        current_task = self.tasks[index]
        
        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Edit Task")
        edit_window.geometry("400x200")
        edit_window.attributes("-topmost", True)  # Keep it on top
        edit_window.focus_force()  # Bring focus to the edit window
        
        edit_entry = ctk.CTkEntry(edit_window, width=300)
        edit_entry.insert(0, current_task['task'])
        edit_entry.pack(pady=10)
        
        edit_priority_var = ctk.StringVar(value=current_task["priority"])
        edit_priority_menu = ctk.CTkOptionMenu(edit_window, variable=edit_priority_var, values = ["High", "Medium","Low"])
        edit_priority_menu.pack(pady=10)
        
        def save_edit():
            new_task_text = edit_entry.get().strip()
            new_priority =  edit_priority_var.get()
            
            if new_task_text:
                
                self.tasks[index]['task'] = new_task_text
                self.tasks[index]['priority'] = new_priority
                self.save_tasks()
                edit_window.destroy()
                self.update_task_list()
        save_button = ctk.CTkButton(edit_window, text="save", command=save_edit)
        save_button.pack(pady=10)
    def toggle_selection(self, index):
        # Toggle the selection state of the task
        if index in self.selected_tasks:
            self.selected_tasks.remove(index)
        else:
            self.selected_tasks.add(index)

        # Update task list to visually reflect the change
        self.update_task_list()

    def mark_selected_done(self):
        for index in self.selected_tasks:
            task = self.tasks[index]
            if not task["done"]:
                task["done"] = True
                task["completed"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.clear_selection()
        
        self.save_tasks()
        self.update_task_list()
        print("Selected tasks marked as done!")
    def mark_selected_undone(self):
        for index in self.selected_tasks:
            task = self.tasks[index]
            if task["done"]:
                task["done"] = False
                task["completed"] = None
                self.clear_selection()
        
        self.save_tasks()
        self.update_task_list()
        print("Selected tasks marked as done!")

    def delete_selected_tasks(self):
        # Delete tasks in reverse order to avoid index shifting issues
        for index in sorted(self.selected_tasks, reverse=True):
            self.tasks.pop(index)

        self.save_tasks()
        self.selected_tasks.clear()  # Clear the selection after deletion
        self.update_task_list()
        print("Selected tasks removed!")

    def save_tasks(self):
        try:
            with open(self.list_path, "w") as file:
                json.dump(self.tasks, file, indent=4)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def load_tasks(self):
        try:
            with open(self.list_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
    def sort_tasks(self, sorting_preference):
        self.sorting_preference = sorting_preference
        self.update_task_list()
        
    def sort_by_prio(self):
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        self.tasks.sort(key=lambda x: priority_order[x['priority']])
    
    def filter_tasks(self, filter_value):
        self.update_task_list()

    def on_enter_key(self, event=None):
        self.add_task()
    def clear_selection(self):
        # Clear the selected tasks
        self.selected_tasks.clear()  # Empty the selection set
        self.update_task_list()  # Refresh the task list to reflect the changes
    def add_category(self):
        category_name = simpledialog.askstring("New Category", "Enter the category name:")
        if not category_name:
            return
        
        colour = colorchooser.askcolor(title="Choose category color")[1]
        if not colour:
            return
        
        self.categories[category_name]=colour
        self.category_menu.configure(values = list(self.categories.keys()))
        self.save_categories()
        
    def save_categories(self):
        with open(self.category_path, "w") as file:
            json.dump(self.categories, file, indent=4)
    def load_categories(self):
        if os.path.exists(self.category_path):
            with open(self.category_path, "r") as file:
                return json.load(file)
        return {"General": "#9AD98D", "Work": "#FFDD57", "Personal": "#FF6666"}
    def create_category_header(self, category):
        category_colors=self.load_categories()
        header_frame = ctk.CTkFrame(self.task_list_frame)
        header_frame.pack(pady=(10,5), fill='x')
        header_color=category_colors.get(category, "#2E2E2E")

        category_label = ctk.CTkLabel(
            header_frame,
            text=category,
            font=("Helvetica", 14, 'bold'),
            text_color='white',
            bg_color=header_color,
            width=0,
            height=30
        )
        category_label.pack(fill='x')
    def load_config(self):
        default_config ={
    "priority": "Medium",
    "category": "General",
    "show_category_colors": True,
    "sorting_preference": "Creation Date",
    "filter_value": "All",
    "window_size": {
        "width": 800,
        "height": 600
    },
    "appearance_mode": "Dark",
    "color_theme": "dark-blue"
    }
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as file:
                return json.load(file)
        return default_config
    def save_config(self):
        data = {
            "priority":self.priority_var.get(),
            "category":self.category_var.get(),
            "show_category_colors": True,
            "sorting_preference": self.sorting_preference,
            "filter_value":self.filter_var.get(),
            "window_size":{
                "width":self.winfo_width(),
                "height": self.winfo_height()
            },
            "appearance_mode": "Dark",
            "color_theme": 'dark-blue'
            
        }
        with open(self.config_path, 'w') as file:
            json.dump(data, file, indent=4)

if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()
