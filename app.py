import tkinter as tk
from tkinter import messagebox
import os

def add_task(event=None):
    task = task_entry.get()
    priority = priority_var.get()
    if task != "":
        color = priority_colors[priority]
        tasks_listbox.insert(tk.END, f"{priority}: {task}")
        tasks_listbox.itemconfig(tk.END, {'fg': color})
        task_entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

def mark_task_done():
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        task_text = tasks_listbox.get(selected_task_index)
        if not task_text.startswith("Done: "):
            tasks_listbox.delete(selected_task_index)
            tasks_listbox.insert(selected_task_index, f"Done: {task_text}")
            tasks_listbox.itemconfig(selected_task_index, {'fg': 'grey'})
            save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task.")

def mark_all_tasks_done():
    tasks = list(tasks_listbox.get(0, tasks_listbox.size()))
    tasks_listbox.delete(0, tk.END)
    for task in tasks:
        if not task.startswith("Done: "):
            task = f"Done: {task}"
        tasks_listbox.insert(tk.END, task)
        tasks_listbox.itemconfig(tk.END, {'fg': 'grey'})
    save_tasks()

def delete_task():
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        tasks_listbox.delete(selected_task_index)
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task.")

def delete_all_tasks():
    tasks_listbox.delete(0, tk.END)
    save_tasks()

def change_task_priority():
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        selected_task = tasks_listbox.get(selected_task_index)
        new_priority = priority_var.get()
        tasks_listbox.delete(selected_task_index)
        tasks_listbox.insert(selected_task_index, f"{new_priority}: {selected_task.split(': ', 1)[1]}")
        color = priority_colors[new_priority]
        tasks_listbox.itemconfig(selected_task_index, {'fg': color})
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task.")

def save_tasks():
    tasks = tasks_listbox.get(0, tasks_listbox.size())
    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(task + "\n")

def load_tasks():
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as file:
            tasks = file.readlines()
            for task in tasks:
                task = task.strip()
                if task.startswith("Done: "):
                    tasks_listbox.insert(tk.END, task)
                    tasks_listbox.itemconfig(tk.END, {'fg': 'grey'})
                else:
                    priority = task.split(': ')[0]
                    color = priority_colors.get(priority, 'black')
                    tasks_listbox.insert(tk.END, task)
                    tasks_listbox.itemconfig(tk.END, {'fg': color})

def sort_tasks():
    tasks = list(tasks_listbox.get(0, tasks_listbox.size()))
    tasks.sort()
    tasks_listbox.delete(0, tk.END)
    for task in tasks:
        if task.startswith("Done: "):
            tasks_listbox.insert(tk.END, task)
            tasks_listbox.itemconfig(tk.END, {'fg': 'grey'})
        else:
            priority = task.split(': ')[0]
            color = priority_colors.get(priority, 'black')
            tasks_listbox.insert(tk.END, task)
            tasks_listbox.itemconfig(tk.END, {'fg': color})
    save_tasks()

root = tk.Tk()
root.title("To-Do List")

root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)

priority_colors = {
    "Low": "green",
    "Mid": "orange",
    "High": "red"
}

input_frame = tk.Frame(root)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
input_frame.columnconfigure(0, weight=1)
input_frame.columnconfigure(1, weight=0)
input_frame.columnconfigure(2, weight=0)
input_frame.columnconfigure(3, weight=0)

task_entry = tk.Entry(input_frame, width=40)
task_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
task_entry.bind("<Return>", add_task)

priority_var = tk.StringVar(value="Mid")
priority_menu = tk.OptionMenu(input_frame, priority_var, "Low", "Mid", "High")
priority_menu.grid(row=0, column=1, padx=5, pady=5)

add_task_button = tk.Button(input_frame, text="Add Task", command=add_task, bg="lightblue")
add_task_button.grid(row=0, column=2, padx=5, pady=5)

change_priority_button = tk.Button(input_frame, text="Change Priority", command=change_task_priority, bg="lightyellow")
change_priority_button.grid(row=0, column=3, padx=5, pady=5)

tasks_listbox = tk.Listbox(root, width=50, height=10)
tasks_listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
button_frame.columnconfigure([0, 1, 2, 3, 4], weight=1)

mark_done_button = tk.Button(button_frame, text="Mark Done", command=mark_task_done, bg="lightgreen")
mark_done_button.grid(row=0, column=0, padx=5, pady=5)

mark_all_done_button = tk.Button(button_frame, text="Mark All Done", command=mark_all_tasks_done, bg="lightgray")
mark_all_done_button.grid(row=0, column=1, padx=5, pady=5)

delete_task_button = tk.Button(button_frame, text="Delete Task", command=delete_task, bg="lightcoral")
delete_task_button.grid(row=0,column=2, padx=5, pady=5)

delete_all_tasks_button = tk.Button(button_frame, text="Delete All Tasks", command=delete_all_tasks, bg="lightpink")
delete_all_tasks_button.grid(row=0, column=3, padx=5, pady=5)

sort_tasks_button = tk.Button(button_frame, text="Sort Tasks", command=sort_tasks, bg="lightyellow")
sort_tasks_button.grid(row=0, column=4, padx=5, pady=5)

load_tasks()

root.mainloop()
