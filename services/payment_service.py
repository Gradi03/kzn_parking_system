from datetime import datetime
from utils.file_handler import load_data, save_data

PARKING_FILE = "database/parking_records.json"
PAYMENTS_FILE = "database/payments.json"

def make_payment(username, mall, amount):
    records = load_data(PARKING_FILE)

    # Mark the unpaid parking record as paid
    for r in records:
        if r["username"] == username and r["mall"] == mall and not r.get("paid", False):
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