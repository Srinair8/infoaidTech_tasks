import tkinter as tk
from tkinter import messagebox

class Task:
    def __init__(self, title, description, status="Incomplete"):
        self.title = title
        self.description = description
        self.status = status

    def mark_complete(self):
        self.status = "Complete"

class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description):
        new_task = Task(title, description)
        self.tasks.append(new_task)

    def delete_task(self, task):
        self.tasks.remove(task)

    def view_tasks(self):
        return self.tasks

    def save_tasks(self, filename="tasks.txt"):
        with open(filename, "w") as file:
            for task in self.tasks:
                file.write(f"{task.title},{task.description},{task.status}\n")

    def load_tasks(self, filename="tasks.txt"):
        self.tasks = []
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
                for line in lines:
                    title, description, status = line.strip().split(',')
                    new_task = Task(title, description, status)
                    self.tasks.append(new_task)
        except FileNotFoundError:
            pass

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("400x400")

        self.todo_list = ToDoList()

        self.title_label = tk.Label(root, text="Title:", font=("Arial", 14))
        self.title_label.pack(pady=5)

        self.title_entry = tk.Entry(root, font=("Arial", 12))
        self.title_entry.pack(pady=5)

        self.description_label = tk.Label(root, text="Description:", font=("Arial", 14))
        self.description_label.pack(pady=5)

        self.description_entry = tk.Entry(root, font=("Arial", 12))
        self.description_entry.pack(pady=5)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task, font=("Arial", 12), bg="#2ecc71", fg="white")
        self.add_button.pack(pady=10)

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task, font=("Arial", 12), bg="#e74c3c", fg="white")
        self.delete_button.pack(pady=10)

        self.view_button = tk.Button(root, text="View Tasks", command=self.view_tasks, font=("Arial", 12), bg="#3498db", fg="white")
        self.view_button.pack(pady=10)

        self.save_button = tk.Button(root, text="Save Tasks", command=self.save_tasks, font=("Arial", 12), bg="#f39c12", fg="white")
        self.save_button.pack(pady=10)

        self.load_button = tk.Button(root, text="Load Tasks", command=self.load_tasks, font=("Arial", 12), bg="#34495e", fg="white")
        self.load_button.pack(pady=10)

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()

        if title and description:
            self.todo_list.add_task(title, description)
            messagebox.showinfo("Success", "Task added successfully.")
        else:
            messagebox.showinfo("Error", "Please enter both title and description.")

    def delete_task(self):
        tasks = self.todo_list.view_tasks()

        if not tasks:
            messagebox.showinfo("Info", "No tasks to delete.")
            return

        selected_task = tasks[0] if len(tasks) == 1 else self.show_task_selection_dialog(tasks)
        
        if selected_task:
            self.todo_list.delete_task(selected_task)
            messagebox.showinfo("Success", "Task deleted successfully.")

    def view_tasks(self):
        tasks = self.todo_list.view_tasks()

        if not tasks:
            messagebox.showinfo("Info", "No tasks to display.")
            return

        tasks_text = "Current Tasks:\n\n"
        for task in tasks:
            tasks_text += f"Title: {task.title}\nDescription: {task.description}\nStatus: {task.status}\n\n"

        messagebox.showinfo("Tasks", tasks_text)

    def save_tasks(self):
        self.todo_list.save_tasks()
        messagebox.showinfo("Success", "Tasks saved successfully.")

    def load_tasks(self):
        self.todo_list.load_tasks()
        messagebox.showinfo("Success", "Tasks loaded successfully.")

    def show_task_selection_dialog(self, tasks):
        selected_task = None

        def on_select():
            nonlocal selected_task
            selected_task = tasks_listbox.get(tk.ACTIVE)
            dialog.destroy()

        dialog = tk.Toplevel(self.root)
        dialog.title("Select Task")

        tasks_listbox = tk.Listbox(dialog)
        tasks_listbox.pack(padx=10, pady=10)

        for task in tasks:
            tasks_listbox.insert(tk.END, task.title)

        select_button = tk.Button(dialog, text="Select", command=on_select, font=("Arial", 12), bg="#3498db", fg="white")
        select_button.pack(pady=10)

        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

        selected_task_index = tasks_listbox.curselection()
        return tasks[selected_task_index[0]] if selected_task_index else None

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
