from datetime import datetime
from pricing.flat_rate import FlatRate
from pricing.hourly_rate import HourlyRate
from pricing.capped_rate import CappedRate
from models.mall import Mall

from services.auth_service import register, login
from services.parking_service import park_vehicle, exit_vehicle, get_customer_history, get_parked_vehicles, sync_mall_capacity, get_mall_records
from services.payment_service import make_payment, get_payment_history
from services.report_service import generate_mall_report, generate_cross_mall_report

# Create malls
gateway = Mall("Gateway", 250, FlatRate())
pavilion = Mall("Pavilion", 180, HourlyRate())
lalucia = Mall("La Lucia", 150, CappedRate())

malls = [gateway, pavilion, lalucia]

# Sync vehicle counts from stored records so capacity is correct after restart
sync_mall_capacity(malls)


def select_mall():
    print("\nSelect Mall:")
    for i, mall in enumerate(malls):
        print(f"{i + 1}. {mall.name}")
    while True:
        try:
            choice = int(input("Choice: ")) - 1
            if 0 <= choice < len(malls):
                return malls[choice]
            print(f"Please enter a number between 1 and {len(malls)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def customer_menu(user):
    mall = select_mall()

    while True:
        print("\nCustomer Menu")
        print("1. Park Vehicle")
        print("2. Exit Vehicle & Pay")
        print("3. View Parking History")
        print("4. View Payment History")
        print("5. Check Current Parking Status")
        print("6. Back")

        choice = input("Choice: ")

        if choice == "1":
            plate = input("Enter licence plate: ").strip().upper()
            if not plate:
                print("Licence plate cannot be empty.")
                continue
            print(park_vehicle(user["username"], mall, plate))

        elif choice == "2":
            fee, pricing = exit_vehicle(user["username"], mall)
            if fee is None:
                print("No active parking to exit.")
                continue

            print(f"\nParking exited. Fee: R{fee} ({pricing})")
            confirm = input("Do you want to pay now? (y/n): ").lower()
            if confirm == "y":
                print(make_payment(user["username"], mall.name, fee))
            else:
                print("Payment pending. You must pay before exiting system.")

        elif choice == "3":
            history = get_customer_history(user["username"])
            if not history:
                print("No parking history found.")
            else:
                for rec in history:
                    status = "Paid" if rec.get("paid") else "Unpaid"
                    print(
                        f"Mall: {rec['mall']}, Entry: {rec['entry_time']}, Exit: {rec.get('exit_time', '-')}, Fee: {rec.get('amount', '-')}, Status: {status}")

        elif choice == "4":
            payments = get_payment_history(user["username"])
            if not payments:
                print("No payment history found.")
            else:
                for pmt in payments:
                    print(f"Mall: {pmt['mall']}, Amount: R{pmt['amount']}, Date: {pmt['timestamp']}")

        elif choice == "5":
            active = [r for r in get_customer_history(user["username"]) if r.get("exit_time") is None]
            if not active:
                print("You are not currently parked anywhere.")
            else:
                for r in active:
                    print(f"Currently parked at {r['mall']} since {r['entry_time']}")

        elif choice == "6":
            break


def admin_menu(user):
    assigned = user.get("assigned_mall")
    mall = next((m for m in malls if m.name == assigned), None)
    if not mall:
        print("No mall assigned to your account. Contact the system owner.")
        return
    print(f"\nAdmin Dashboard - {mall.name}")
    print(f"Capacity: {mall.current_vehicles}/{mall.capacity}")

    vehicles = get_parked_vehicles(mall.name)
    print("\nCurrently Parked Vehicles:")
    if not vehicles:
        print("None")
    else:
        for v in vehicles:
            plate = v.get('licence_plate', 'N/A')
            print(f"- {v['username']} | Plate: {plate} | Entered: {v['entry_time']}")

    # Daily activity summary
    today = datetime.now().date()
    all_today = [
        r for r in get_mall_records(mall.name)
        if datetime.strptime(r["entry_time"], "%Y-%m-%d %H:%M:%S").date() == today
    ]
    total_parked_today, total_revenue_today = len(all_today), sum(r.get("amount", 0) for r in all_today)
    print(f"\nDaily Activity Summary ({datetime.now().strftime('%Y-%m-%d')})")
    print(f"Vehicles entered today: {total_parked_today}")
    print(f"Revenue collected today: R{total_revenue_today}")

    # Full mall report
    total_vehicles, total_revenue, avg_duration = generate_mall_report(mall.name)
    print(f"\nAll-Time Mall Report")
    print(f"Total vehicles parked: {total_vehicles}")
    print(f"Total revenue: R{total_revenue}")
    print(f"Average parking duration: {avg_duration} hours")


def owner_menu():
    print("\nOwner Dashboard - All Malls")
    cross_report = generate_cross_mall_report(malls)
    for mall_data in cross_report:
        print(f"\n{mall_data['name']}")
        print(f"Vehicles: {mall_data['vehicles']}")
        print(f"Revenue: R{mall_data['revenue']}")
        print(f"Average Parking Duration: {mall_data['average_duration']} hours")


def main():
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choice: ")

        if choice == "1":
            u = input("Username: ").strip()
            p = input("Password: ").strip()
            r = input("Role (customer/admin/owner): ").strip().lower()
            if r not in ("customer", "admin", "owner"):
                print("Invalid role. Choose: customer, admin, or owner.")
                continue
            assigned_mall = None
            if r == "admin":
                print("Select assigned mall:")
                for i, m in enumerate(malls):
                    print(f"{i + 1}. {m.name}")
                while True:
                    try:
                        idx = int(input("Choice: ")) - 1
                        if 0 <= idx < len(malls):
                            assigned_mall = malls[idx].name
                            break
                        print(f"Please enter a number between 1 and {len(malls)}.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            print(register(u, p, r, assigned_mall))

        elif choice == "2":
            u = input("Username: ")
            p = input("Password: ")

            user = login(u, p)

            if user:
                if user["role"] == "customer":
                    customer_menu(user)
                elif user["role"] == "admin":
                    admin_menu(user)
                elif user["role"] == "owner":
                    owner_menu()
            else:
                print("Invalid login")

        elif choice == "3":
            break

if __name__ == "__main__":
    main()