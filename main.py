from datetime import datetime
from pricing.flat_rate import FlatRate
from pricing.hourly_rate import HourlyRate
from pricing.capped_rate import CappedRate
from models.mall import Mall

from services.auth_service import register, login
from services.parking_service import park_vehicle, exit_vehicle, get_customer_history, get_parked_vehicles
from services.payment_service import make_payment
from services.report_service import generate_mall_report, generate_cross_mall_report

# Create malls
gateway = Mall("Gateway", 250, FlatRate())
pavilion = Mall("Pavilion", 180, HourlyRate())
lalucia = Mall("La Lucia", 150, CappedRate())

malls = [gateway, pavilion, lalucia]


def select_mall():
    print("\nSelect Mall:")
    for i, mall in enumerate(malls):
        print(f"{i + 1}. {mall.name}")
    choice = int(input("Choice: ")) - 1
    return malls[choice]


def customer_menu(user):
    mall = select_mall()

    while True:
        print("\nCustomer Menu")
        print("1. Park Vehicle")
        print("2. Exit Vehicle & Pay")
        print("3. View History")
        print("4. Back")

        choice = input("Choice: ")

        if choice == "1":
            print(park_vehicle(user["username"], mall))

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
            break


def admin_menu():
    mall = select_mall()
    print(f"\nAdmin Dashboard - {mall.name}")
    print(f"Capacity: {mall.current_vehicles}/{mall.capacity}")

    vehicles = get_parked_vehicles(mall.name)
    print("Currently Parked Vehicles:")
    if not vehicles:
        print("None")
    else:
        for v in vehicles:
            print(f"- {v['username']} entered at {v['entry_time']}")

    # Optional: Daily activity summary
    total_parked_today = sum(
        1 for v in vehicles if datetime.strptime(v["entry_time"], "%Y-%m-%d %H:%M:%S").date() == datetime.now().date())
    print(f"Vehicles parked today: {total_parked_today}")


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
            u = input("Username: ")
            p = input("Password: ")
            r = input("Role (customer/admin/owner): ")
            print(register(u, p, r))

        elif choice == "2":
            u = input("Username: ")
            p = input("Password: ")

            user = login(u, p)

            if user:
                if user["role"] == "customer":
                    customer_menu(user)
                elif user["role"] == "admin":
                    admin_menu()
                elif user["role"] == "owner":
                    owner_menu()
            else:
                print("Invalid login")

        elif choice == "3":
            break
1

if __name__ == "__main__":
    main()