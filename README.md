# KZN Parking Management System

A command-line Parking Management System developed for a property management company operating across KwaZulu-Natal, South Africa. The system standardises parking operations across multiple shopping malls, supporting three user roles with distinct access privileges.

---

## How to Run

### Requirements

- Python 3.8 or later
- No third-party packages required (standard library only)

### Steps

```bash
# 1. Navigate to the project folder
cd kzn_parking_system

# 2. Run the application
python main.py
```

---

## Project Structure

```
kzn_parking_system/
├── main.py                     # Entry point — menus and application flow
├── models/
│   ├── mall.py                 # Mall entity (name, capacity, pricing strategy)
│   ├── parking.py              # ParkingRecord entity
│   └── user.py                 # User entity
├── pricing/
│   ├── base_pricing.py         # Abstract PricingStrategy base class
│   ├── flat_rate.py            # Flat Rate — R15 per visit (Gateway)
│   ├── hourly_rate.py          # Hourly Rate — R10/hour, ceil (Pavilion)
│   └── capped_rate.py          # Capped Rate — R12/hour, max R60 (La Lucia)
├── services/
│   ├── auth_service.py         # Registration and login (SHA-256 hashed passwords)
│   ├── parking_service.py      # Vehicle entry, exit, capacity, history
│   ├── payment_service.py      # Payment processing and history
│   └── report_service.py       # Mall-level and cross-mall reporting
├── utils/
│   └── file_handler.py         # JSON read/write persistence helpers
└── database/
    ├── users.json              # Stored user accounts
    ├── parking_records.json    # Parking session records
    └── payments.json           # Payment records
```

---

## User Roles

### 1. Customer

- Register an account with a username, password, and role `customer`
- Log in and select a mall
- Park a vehicle (enter licence plate)
- Exit and view the calculated fee and pricing type before paying
- Make payment and receive confirmation
- View full parking history and payment history
- Check current active parking status

### 2. Parking Administrator

- Register with role `admin` — must be assigned to one specific mall during registration
- Log in to see their mall's dashboard only:
  - Current occupancy vs. capacity
  - List of all currently parked vehicles (username + licence plate + entry time)
  - Daily activity summary (vehicles entered today, revenue collected today)
  - All-time mall report (total vehicles, total revenue, average duration)

### 3. Owner / Shareholder

- Register with role `owner`
- Log in to view a cross-mall comparative report showing, for each mall:
  - Total vehicles parked (all time)
  - Total revenue generated
  - Average parking duration

---

## Malls and Pricing

| Mall                        | Location          | Capacity | Pricing Rule                                     |
| --------------------------- | ----------------- | -------- | ------------------------------------------------ |
| Gateway Theatre of Shopping | Umhlanga, Durban  | 250      | Flat Rate — R15 per visit                        |
| Pavilion Shopping Centre    | Westville, Durban | 180      | Hourly Rate — R10/hour (part thereof rounds up)  |
| La Lucia Mall               | La Lucia, Durban  | 150      | Hourly Rate with Cap — R12/hour, maximum R60/day |

**Pricing examples:**

- Gateway: any duration = **R15**
- Pavilion: 90 minutes → 2 hours → **R20**
- La Lucia: 7 hours → R84 → capped at **R60**

---

## Design Decisions

### Strategy Pattern for Pricing

All pricing logic is isolated in `pricing/`. Each mall receives a pricing strategy object at startup. Adding a new pricing model requires only creating a new class that extends `PricingStrategy` in `base_pricing.py` and implementing `calculate_fee(hours)` and `get_type()` — no other files need to change.

### Data Persistence

All data is stored as JSON in `database/`. The system reloads data on every operation and re-syncs mall vehicle counts from stored records on startup via `sync_mall_capacity()`, ensuring correctness across program restarts.

### Password Security

Passwords are hashed with SHA-256 using Python's built-in `hashlib` before being stored. Plain-text passwords are never written to disk.

### Admin Scoping

Admins are assigned to a single mall during registration. Their dashboard only ever shows data for that mall — they cannot select or view other malls.

---

## Testing Guide for Lecturers

Below is a suggested sequence to demonstrate all functionality:

### Step 1 — Register accounts

Run `python main.py` and register three accounts:

- Role `customer`, any username/password
- Role `admin`, any username/password — select **Pavilion** as the assigned mall
- Role `owner`, any username/password

### Step 2 — Customer: Park and Pay

1. Log in as the customer
2. Select **Gateway** mall
3. Choose **Park Vehicle**, enter a licence plate (e.g. `KZN 123 GP`)
4. Choose **Exit Vehicle & Pay** — observe the fee displayed as **R15 (Flat Rate)**
5. Confirm payment and view Payment History

Repeat with **Pavilion** for an hourly fee (exit after a short time — minimum 1 hour = R10).

### Step 3 — Admin dashboard

1. Log in as the admin (assigned to Pavilion)
2. Observe the dashboard — current occupancy, parked vehicles with licence plates, daily summary

### Step 4 — Owner report

1. Log in as the owner
2. Observe the cross-mall report comparing all three malls

### Step 5 — Capacity enforcement

Park vehicles until a mall reaches capacity and verify the system blocks further entry.

---

## Data Reset

To start with a clean database, replace the contents of each file in `database/` with `[]`:

```bash
python -c "open('database/users.json','w').write('[]'); open('database/parking_records.json','w').write('[]'); open('database/payments.json','w').write('[]')"
```
