from datetime import datetime
from utils.file_handler import load_data, save_data

PARKING_FILE = "database/parking_records.json"


def park_vehicle(username, mall, licence_plate):
    records = load_data(PARKING_FILE)

    # Check if user already has an active parking session at this mall
    for r in records:
        if r["username"] == username and r["mall"] == mall.name and r.get("exit_time") is None:
            return "You already have an active parking session at this mall."

    if mall.current_vehicles >= mall.capacity:
        return "Mall parking is full."

    record = {
        "username": username,
        "mall": mall.name,
        "licence_plate": licence_plate,
        "entry_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "exit_time": None,
        "amount": 0,
        "paid": False
    }

    records.append(record)
    save_data(PARKING_FILE, records)
    mall.current_vehicles += 1
    return f"Vehicle parked at {mall.name}."


def exit_vehicle(username, mall):
    records = load_data(PARKING_FILE)

    for r in records:
        if r["username"] == username and r["mall"] == mall.name and r.get("exit_time") is None:
            exit_time = datetime.now()
            entry_time = datetime.strptime(r["entry_time"], "%Y-%m-%d %H:%M:%S")
            hours = (exit_time - entry_time).total_seconds() / 3600

            fee = mall.pricing_strategy.calculate_fee(hours)
            pricing = mall.pricing_strategy.get_type()

            r["exit_time"] = exit_time.strftime("%Y-%m-%d %H:%M:%S")
            r["amount"] = fee

            save_data(PARKING_FILE, records)
            mall.current_vehicles = max(0, mall.current_vehicles - 1)
            return fee, pricing

    return None, None


def get_customer_history(username):
    records = load_data(PARKING_FILE)
    return [r for r in records if r["username"] == username]


def get_parked_vehicles(mall_name):
    records = load_data(PARKING_FILE)
    return [r for r in records if r["mall"] == mall_name and r.get("exit_time") is None]


def get_mall_records(mall_name):
    """Return all parking records for a given mall."""
    records = load_data(PARKING_FILE)
    return [r for r in records if r["mall"] == mall_name]


def sync_mall_capacity(malls):
    """Sync mall.current_vehicles from stored parking records on startup."""
    records = load_data(PARKING_FILE)
    active_counts = {}
    for r in records:
        if r.get("exit_time") is None:
            active_counts[r["mall"]] = active_counts.get(r["mall"], 0) + 1
    for mall in malls:
        mall.current_vehicles = active_counts.get(mall.name, 0)