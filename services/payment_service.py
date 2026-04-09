from datetime import datetime
from utils.file_handler import load_data, save_data

PARKING_FILE = "database/parking_records.json"
PAYMENTS_FILE = "database/payments.json"

def make_payment(username, mall, amount):
    records = load_data(PARKING_FILE)

    # Mark the most recently exited unpaid record for this user/mall
    for r in sorted(records, key=lambda x: x.get("exit_time") or "", reverse=True):
        if r["username"] == username and r["mall"] == mall and r.get("exit_time") and not r.get("paid", False):
            r["paid"] = True
            save_data(PARKING_FILE, records)
            break

    payments = load_data(PAYMENTS_FILE)
    payments.append({
        "username": username,
        "mall": mall,
        "amount": amount,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_data(PAYMENTS_FILE, payments)
    return f"Payment successful for R{amount}"


def get_payment_history(username):
    """Return all payment records for a given customer."""
    payments = load_data(PAYMENTS_FILE)
    return [p for p in payments if p["username"] == username]