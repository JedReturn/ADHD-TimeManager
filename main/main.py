import json
import matplotlib.pyplot as plt
import io
import os
from PIL import Image

#global vars
global current_list
global current_filter
current_list = 'tasks'
path = os.getcwd().replace('\\','/')
def main():
    with open(path +'/data/tasks.json', 'r') as f:
        tasks = json.load(f)
    with open(path +'/data/stored_tasks.json', 'r') as f:
        stored = json.load(f)
    return tasks, stored
tasks, stored = main()

def save():
    with open(path +'/data/tasks.json', 'w') as f:
        json.dump(tasks, f, indent=2)
    with open(path +'/data/stored_tasks.json', 'w') as f:
        json.dump(stored, f, indent=2)


def get_tasks(name):
    if name == 'stored':
        return stored
    elif name == 'tasks':
        return tasks

def get_index(name, list):
    tasks = get_tasks(list)
    for task in tasks:
        if task['name'] == name:
            return tasks.index(task)

def complete_task(index, list):
    tasks = get_tasks(list)
    tasks[index]['complete'] = not tasks[index]['complete']

def remove_task(index, list):
    tasks = get_tasks(list)
    tasks.pop(index)

def add_task(task, list):
    tasks = get_tasks(list)
    tasks.append(task)



#Filters
def all_filter(task):
    if task:
        return True
    
def completed_filter(task):
    if task['complete'] == True:
        return True
    return False

def incomplete_filter(task):
    if task['complete'] == False:
        return True
    return False

current_filter = incomplete_filter

def get_globals():
    global current_list, current_filter
    return current_list, current_filter

def change_globals(list_name, filter):
    global current_list, current_filter
    current_list, current_filter = list_name, filter

def filter_list():
    global current_filter, current_list
    ls = get_tasks(current_list)
    filtered_list = []
    for i in ls:
        if current_filter(i):
            filtered_list.append(i)
    return filtered_list

def generate_pie_chart_image(tasks):
    pie_data = {}
    ls = filter_list()
    for task in ls:
        t = task['task_type']
        pie_data[t] = pie_data.get(t, 0) + int(task['est'])


    if not pie_data:
        return None, 0

    labels = list(pie_data.keys())
    sizes = list(pie_data.values())
    total = sum(sizes)

    # Format labels with task type and actual minutes
    label_texts = [f"{label} ({value}m)" for label, value in zip(labels, sizes)]

    # Function for showing both percentage and minutes
    def format_label(pct, all_vals):
        absolute = int(round(pct * sum(all_vals) / 100.0))
        return f"{pct:.1f}%\n({absolute}m)"

    fig, ax = plt.subplots(figsize=(3, 3)) 
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=label_texts,
        autopct=lambda pct: format_label(pct, sizes),
        startangle=90
    )
    ax.axis('equal')
    plt.figtext(0.5, 0.01, f"Total: {total} minutes", ha='center', fontsize=10)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf), total


#init globals


