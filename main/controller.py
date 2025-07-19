import main
import json


global filter_index

tasks, stored = main.main()
filter_index = []



def filter_list():
    current_list, current_filter = main.get_globals()
    global filter_index
    ls = main.get_tasks(current_list)
    filtered_list = []
    filter_index = []
    for i in ls:
        if current_filter(i):
            filtered_list.append(i)
            filter_index.append(ls.index(i))
    return filtered_list


def complete_selected(index):
    true_index = filter_index[index]
    main.complete_task(true_index)
