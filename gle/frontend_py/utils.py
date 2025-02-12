import json


def load_progress():

    with open('progress.json', 'r') as f:
        progress = json.load(f)

    return progress


def write_progress(progress):

    with open('progress.json', 'w') as f:
        json.dump(progress, f)


def read_progress():

    progress = load_progress()

    return progress['current']/progress['total']


def get_tool_state(tool_name: str):

    progress = load_progress()

    if progress['tools'][tool_name]['available']:
        return 'normal'
    else:
        return 'disabled'
    

def increment_progress():

    progress = load_progress()

    progress['current'] += 1

    write_progress(progress)
