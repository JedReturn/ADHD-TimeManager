import tkinter as tk
from tkinter import messagebox
from tkinter import Toplevel, Label
from PIL import ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import json
import main
import controller
from datetime import datetime


tasks = main.get_tasks('tasks')
root = tk.Tk()
root.title("Task Manager")
root.geometry("500x550")


# Create main layout frames


top_left_frame = tk.Frame(root)
top_center_frame = tk.Frame(root)
top_right_frame = tk.Frame(root)
middle_frame = tk.Frame(root)
bottom_frame = tk.Frame(root)


top_left_frame.place(relx=0, rely=0, relwidth=.2, relheight=.3)
top_center_frame.place(relx=.2, rely=0, relwidth=.6, relheight=.3)
top_right_frame.place(relx=.8, rely=0, relwidth=.2, relheight=.3)
middle_frame.place(relx=0, rely=.3, relwidth=1, relheight=.1)
bottom_frame.place(relx=0, rely=.4, relwidth=1, relheight=.6)

task_listbox = tk.Listbox(top_center_frame, width=50)

#Update
def update_list(box=task_listbox):
    ls = controller.filter_list()
    box.delete(0, tk.END)
    for i in ls:    
        box.insert(tk.END, f"{i['name']}: {i['task_type']} {i['priority']} {i['est']}")

def update_pie_chart_display():
    image, total = main.generate_pie_chart_image(tasks)
    if image is None:
        pie_chart_label.config(image='', text='No tasks to display')
        pie_chart_label.image = None
        return

    chart_img = ImageTk.PhotoImage(image)
    pie_chart_label.config(image=chart_img, text='')
    pie_chart_label.image = chart_img  # Save reference!


def update_all():
    update_list()
    update_pie_chart_display()


def change_filter(filter):
    current_list, current_filter = main.get_globals()
    main.change_globals(current_list, filter)
    update_all()


def change_list(list_name):
    current_list, current_filter = main.get_globals()
    main.change_globals(list_name, current_filter)
    update_all()



def open_add_task_popup():
    popup = tk.Toplevel(root)
    popup.title("Add New Task")
    popup.geometry("600x600")  # You can adjust the size

    def on_tempbox_select(event):
        i = get_selected_task(temp_listbox)
        if i:
            index = main.get_index(i, 'stored')
            tasks = main.get_tasks('stored')
            new_task = tasks[index]
            name, task, est = new_task['name'], new_task['task_type'], new_task['est']
            name_entry.delete(0, tk.END) ; type_entry.delete(0, tk.END) ; est_entry.delete(0, tk.END)  
            name_entry.insert(0, name) ; type_entry.insert(0, task) ; est_entry.insert(0, est)

    # Task name
    tk.Label(popup, text="Task Name").pack()
    name_entry = tk.Entry(popup)
    name_entry.bind("<<ListboxSelect>>", on_tempbox_select)
    name_entry.pack()

    # Task type
    tk.Label(popup, text="Task Type").pack()
    type_entry = tk.Entry(popup)
    type_entry.bind("<<ListboxSelect>>", on_tempbox_select)
    type_entry.pack()

    # Priority (Radio buttons)
    tk.Label(popup, text="Priority").pack()
    priority_var = tk.IntVar(value=1)
    for i in range(1, 5):
        tk.Radiobutton(popup, text=str(i), variable=priority_var, value=i).pack()

    # Estimated time
    tk.Label(popup, text="Estimated Time (minutes)").pack()
    est_entry = tk.Entry(popup)
    est_entry.bind("<<ListboxSelect>>", on_tempbox_select)
    est_entry.pack()

    temp_listbox = tk.Listbox(popup, width=50)
    temp_listbox.bind("<<ListboxSelect>>", on_tempbox_select)
    temp_listbox.pack(pady=10)
    change_list('stored')
    change_filter(main.all_filter)
    update_list(box=temp_listbox)


    # Submit button
    def submit_task():
        name = name_entry.get()
        task_type = type_entry.get()
        est = est_entry.get()
        if not name or not task_type or not est.isdigit():
            messagebox.showerror("Invalid Input", "Please fill in all fields correctly.")
            return

        new_task = {
            "name": name,
            "task_type": task_type,
            "priority": priority_var.get(),
            "est": int(est),
            "complete": False
            }

        main.add_task(new_task, 'tasks')
        change_list('tasks')
        update_all()
        popup.destroy()

    tk.Button(popup, text="Add Task", command=submit_task).pack(pady=10)
#Misc/////////////////////////////////////////////
def get_selected_task(box=task_listbox):
    i = box.curselection()
    return i

#Comands
def complete_selected():
    index = get_selected_task()
    controller.complete_selected(index[0])
    update_all()

def remove_selected():
    current_list, current_filter = main.get_globals()
    name = get_selected_task()
    index = main.get_index(name, current_list)
    main.remove_task(index, current_list)
    update_all()

def store_selected():
    current_list, current_filter = main.get_globals()
    if not current_list == 'tasks':
        pass
    else:
        name = get_selected_task()
        index = main.get_index(name, 'tasks')
        tasks = main.get_tasks('tasks')
        task = tasks[index]
        task['complete'] = False
        main.add_task(task, 'stored')
        update_all()

def on_listbox_select(event):
    selected = task_listbox.curselection()
    if selected:
        remove_button.config(state=tk.NORMAL)
        store_button.config(state=tk.NORMAL)
        complete_button.config(state=tk.NORMAL)
    else:
        remove_button.config(state=tk.DISABLED)
        store_button.config(state=tk.DISABLED)
        complete_button.config(state=tk.DISABLED)

#listbox
task_listbox.bind("<<ListboxSelect>>", on_listbox_select)
task_listbox.place(in_=top_center_frame, relheight=1, relwidth=1)

#Buttons
remove_button = tk.Button(top_left_frame, text="Remove", command=remove_selected, state=tk.DISABLED)
remove_button.place(in_=top_left_frame, relheight=.33, relwidth=1, rely=0)

store_button = tk.Button(top_left_frame, text="Store", command=store_selected, state=tk.DISABLED)
store_button.place(in_=top_left_frame, relheight=.34, relwidth=1, rely=.33)

complete_button = tk.Button(top_left_frame, text="Complete", command=lambda:complete_selected(), state=tk.DISABLED)
complete_button.place(in_=top_left_frame, relheight=.33, relwidth=1, rely=.67)

remove_button.bind("<<ListboxSelect>>", on_listbox_select)
store_button.bind("<<ListboxSelect>>", on_listbox_select)
complete_button.bind("<<ListboxSelect>>", on_listbox_select)

buttons = [
    ("Completed filter", lambda:change_filter(main.completed_filter), tk.NORMAL),
    ("Incomplete filter", lambda:change_filter(main.incomplete_filter), tk.NORMAL),
    ("All filter", lambda:change_filter(main.all_filter), tk.NORMAL),
    ("Task list", lambda:change_list('tasks'), tk.NORMAL),
    ("Stored list", lambda:change_list('stored'), tk.NORMAL)
]

for i, (label, func, s) in enumerate(buttons):
    tk.Button(top_right_frame, text=label, width=12, command=func, state=s).place(in_=top_right_frame, relheight=.2, relwidth=1, rely=(i*0.2))


clock_label = tk.Label(middle_frame, font=('Consolas', 24), fg='black')
clock_label.place(in_=middle_frame, relheight=1, relwidth=.34, relx=.33)

add_button = tk.Button(middle_frame, text="Add Task", command=open_add_task_popup)
add_button.place(in_=middle_frame, relheight=1, relwidth=.33, relx=0)

Save_all_button = tk.Button(middle_frame, text="Save all", command=main.save)
Save_all_button.place(in_=middle_frame, relheight=1, relwidth=.33, relx=.67)


#STARTUP
pie_chart_frame = tk.Frame(bottom_frame)
pie_chart_frame.place(in_=bottom_frame, relheight=1, relwidth=1)

pie_chart_label = tk.Label(bottom_frame)
pie_chart_label.place(in_=bottom_frame, relheight=1, relwidth=1)


update_all()

def update_clock():
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')  # 24-hour format
    clock_label.config(text=current_time)
    root.after(1000, update_clock)  # Call again in 1000ms (1s)

root.lift()
root.attributes('-topmost', True)
root.after_idle(root.attributes, '-topmost', False)

update_clock()
root.mainloop()
