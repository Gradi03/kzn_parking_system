import hashlib
from utils.file_handler import load_data, save_data

FILE = "database/users.json"


def _hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register(username, password, role, assigned_mall=None):
    users = load_data(FILE)

    for u in users:
        if u["username"] == username:
            return "Username already exists."

    user_record = {
        "username": username,
        "password": _hash_password(password),
        "role": role
    }
    if assigned_mall:
        user_record["assigned_mall"] = assigned_mall

    users.append(user_record)
    save_data(FILE, users)
    return "Registered successfully."


def login(username, password):
    users = load_data(FILE)
    hashed = _hash_password(password)

    for u in users:
        if u["username"] == username and u["password"] == hashed:
            return u

    return None