from utils.file_handler import load_data, save_data

FILE = "database/users.json"

def register(username, password, role):
    users = load_data(FILE)

    for u in users:
        if u["username"] == username:
            return "User exists"

    users.append({
        "username": username,
        "password": password,
        "role": role
    })

    save_data(FILE, users)
    return "Registered successfully"

def login(username, password):
    users = load_data(FILE)

    for u in users:
        if u["username"] == username and u["password"] == password:
            return u

    return None