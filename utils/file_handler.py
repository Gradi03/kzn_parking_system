import json

def load_data(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)