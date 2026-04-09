from datetime import datetime
from utils.file_handler import load_data

PARKING_FILE = "database/parking_records.json"

def generate_mall_report(mall_name):
    """Return total vehicles, total revenue, average parking duration for a mall"""
    records = load_data(PARKING_FILE)

    mall_records = [r for r in records if r["mall"] == mall_name and r.get("exit_time")]

    total_vehicles = len(mall_records)
    total_revenue = sum(r.get("amount", 0) for r in mall_records)

    # Average duration in hours
    durations = []
    for r in mall_records:
        entry = datetime.fromisoformat(r["entry_time"])
        exit_time = datetime.fromisoformat(r["exit_time"])
        durations.append((exit_time - entry).total_seconds() / 3600)

    average_duration = round(sum(durations)/len(durations), 2) if durations else 0

    return total_vehicles, total_revenue, average_duration

def generate_cross_mall_report(malls):
    """Return list of reports for all malls"""
    report = []
    for mall in malls:
        vehicles, revenue, avg_duration = generate_mall_report(mall.name)
        report.append({
            "name": mall.name,
            "vehicles": vehicles,
            "revenue": revenue,
            "average_duration": avg_duration
        })
    return report