"""
Generates synthetic raw data for the Enterprise BI Platform.
Run once to create CSVs under data/raw/ that the ETL pipelines consume.

Why synthetic data with deliberate mess:
Real source systems are never clean. We inject nulls, duplicates, and
inconsistent formats on purpose so the ETL layer has real work to do
(dedupe, null-handling, type casting). If you can't explain WHY a
cleaning step exists, that's a gap to close before an interview.
"""
import random
import uuid
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

N_CUSTOMERS = 500
N_EMPLOYEES = 25
N_PRODUCTS = 150
N_SUPPLIERS = 20
N_ORDERS = 4000
N_RETURNS = 300
DAYS_BACK = 365

OUT = "data/raw"
import os
os.makedirs(OUT, exist_ok=True)

REGIONS = ["North", "South", "East", "West", "Central"]
CATEGORIES = ["Electronics", "Apparel", "Home & Kitchen", "Sports", "Books", "Toys", "Beauty"]


def gen_customers():
    rows = []
    for i in range(1, N_CUSTOMERS + 1):
        rows.append({
            "customer_id": i,
            "customer_name": fake.name(),
            "email": fake.email() if random.random() > 0.03 else None,  # some nulls
            "region": random.choice(REGIONS),
            "signup_date": fake.date_between(start_date="-3y", end_date="-30d"),
            "segment": random.choice(["Retail", "Wholesale", "Enterprise"]),
        })
    df = pd.DataFrame(rows)
    # inject duplicate rows (common real-world issue)
    dupes = df.sample(15, random_state=1)
    df = pd.concat([df, dupes], ignore_index=True)
    df.to_csv(f"{OUT}/customers.csv", index=False)
    return df


def gen_employees():
    rows = []
    for i in range(1, N_EMPLOYEES + 1):
        rows.append({
            "employee_id": i,
            "employee_name": fake.name(),
            "region": random.choice(REGIONS),
            "hire_date": fake.date_between(start_date="-5y", end_date="-60d"),
            "role": random.choice(["Sales Rep", "Account Manager", "Regional Lead"]),
        })
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}/employees.csv", index=False)
    return df


def gen_suppliers():
    rows = []
    for i in range(1, N_SUPPLIERS + 1):
        rows.append({
            "supplier_id": i,
            "supplier_name": fake.company(),
            "country": fake.country(),
            "reliability_score": round(random.uniform(0.7, 1.0), 2),
        })
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}/suppliers.csv", index=False)
    return df


def gen_products(suppliers_df):
    rows = []
    for i in range(1, N_PRODUCTS + 1):
        cost = round(random.uniform(5, 300), 2)
        rows.append({
            "product_id": i,
            "product_name": fake.word().capitalize() + " " + random.choice(
                ["Pro", "Max", "Lite", "Plus", "Standard"]),
            "category": random.choice(CATEGORIES),
            "supplier_id": random.choice(suppliers_df["supplier_id"].tolist()),
            "unit_cost": cost,
            "unit_price": round(cost * random.uniform(1.2, 2.5), 2),
            "reorder_threshold": random.randint(10, 50),
        })
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}/products.csv", index=False)
    return df


def gen_inventory(products_df):
    rows = []
    for _, p in products_df.iterrows():
        rows.append({
            "product_id": p["product_id"],
            "warehouse_region": random.choice(REGIONS),
            "stock_on_hand": random.randint(0, 500),
            "last_restock_date": fake.date_between(start_date="-90d", end_date="today"),
            "snapshot_date": datetime.today().date(),
        })
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}/inventory_snapshots.csv", index=False)
    return df


def gen_orders(customers_df, employees_df, products_df):
    valid_customers = customers_df["customer_id"].unique().tolist()
    valid_employees = employees_df["employee_id"].unique().tolist()
    valid_products = products_df.set_index("product_id")

    order_rows, line_rows = [], []
    for oid in range(1, N_ORDERS + 1):
        cust = random.choice(valid_customers)
        emp = random.choice(valid_employees)
        order_date = fake.date_between(start_date=f"-{DAYS_BACK}d", end_date="today")
        n_lines = random.randint(1, 5)
        status = random.choices(
            ["Completed", "Completed", "Completed", "Cancelled", "Pending"],
            weights=[70, 10, 10, 5, 5])[0]

        order_rows.append({
            "order_id": oid,
            "customer_id": cust,
            "employee_id": emp,
            "order_date": order_date,
            "status": status,
            "region": random.choice(REGIONS),
        })

        for _ in range(n_lines):
            pid = random.choice(valid_products.index.tolist())
            qty = random.randint(1, 10)
            unit_price = valid_products.loc[pid, "unit_price"]
            # occasional bad data: negative qty typo, missing price
            if random.random() < 0.01:
                qty = -abs(qty)
            line_rows.append({
                "order_line_id": str(uuid.uuid4())[:8],
                "order_id": oid,
                "product_id": pid,
                "quantity": qty,
                "unit_price": unit_price if random.random() > 0.02 else None,
            })

    orders_df = pd.DataFrame(order_rows)
    lines_df = pd.DataFrame(line_rows)
    orders_df.to_csv(f"{OUT}/orders.csv", index=False)
    lines_df.to_csv(f"{OUT}/order_lines.csv", index=False)
    return orders_df, lines_df


def gen_returns(orders_df, lines_df):
    sample_lines = lines_df.sample(min(N_RETURNS, len(lines_df)), random_state=2)
    rows = []
    for i, (_, line) in enumerate(sample_lines.iterrows(), start=1):
        rows.append({
            "return_id": i,
            "order_id": line["order_id"],
            "product_id": line["product_id"],
            "return_date": fake.date_between(start_date="-180d", end_date="today"),
            "reason": random.choice(
                ["Defective", "Wrong Item", "No Longer Needed", "Late Delivery", "Other"]),
            "quantity_returned": max(1, int(abs(line["quantity"] or 1) * random.uniform(0.2, 1.0))),
        })
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}/returns.csv", index=False)
    return df


if __name__ == "__main__":
    customers = gen_customers()
    employees = gen_employees()
    suppliers = gen_suppliers()
    products = gen_products(suppliers)
    inventory = gen_inventory(products)
    orders, lines = gen_orders(customers, employees, products)
    returns = gen_returns(orders, lines)
    print("Generated raw data in data/raw/:")
    for f in os.listdir(OUT):
        print(" -", f)
