"""
MEMBER 1 — Sales & Customer Analytics ETL
Owns: customers, employees, orders, order_lines (raw -> staging)

Pipeline stages (this is what you explain in the interview):
1. EXTRACT   — Read source CSV files
2. LOAD RAW  — Store original data in raw schema
3. VALIDATE  — Check data quality
4. CLEAN     — Remove duplicates, fix nulls, convert types
5. TRANSFORM — Create derived fields
6. LOAD      — Store cleaned data in staging schema

This is the function Airflow's sales_dag.py calls as a task.
"""
import pandas as pd
from db import load_df

RAW = "data/raw"


def extract():
    customers = pd.read_csv(f"{RAW}/customers.csv")
    employees = pd.read_csv(f"{RAW}/employees.csv")
    orders = pd.read_csv(f"{RAW}/orders.csv")
    order_lines = pd.read_csv(f"{RAW}/order_lines.csv")
    return customers, employees, orders, order_lines


def validate(customers, orders, order_lines):
    issues = []
    if customers["customer_id"].isna().any():
        issues.append("customers: null customer_id found")
    if not order_lines["order_id"].isin(orders["order_id"]).all():
        issues.append("order_lines: orphan order_id references found")
    if issues:
        print("VALIDATION WARNINGS:")
        for i in issues:
            print(" -", i)
    return issues


def clean_customers(customers: pd.DataFrame) -> pd.DataFrame:
    df = customers.drop_duplicates(subset=["customer_id"]).copy()
    df["email"] = df["email"].fillna("unknown@noemail.com")
    df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
    df = df.dropna(subset=["customer_name"])
    return df


def clean_employees(employees: pd.DataFrame) -> pd.DataFrame:
    df = employees.drop_duplicates(subset=["employee_id"]).copy()
    df["hire_date"] = pd.to_datetime(df["hire_date"], errors="coerce")
    return df


def clean_orders(orders: pd.DataFrame) -> pd.DataFrame:
    df = orders.drop_duplicates(subset=["order_id"]).copy()
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"])
    return df


def clean_order_lines(order_lines: pd.DataFrame) -> pd.DataFrame:
    df = order_lines.drop_duplicates(subset=["order_line_id"]).copy()
    # drop bad-data rows: negative quantity is a data entry error, not a real return
    df = df[df["quantity"] > 0]
    # impute missing unit_price with the median price for that product
    df["unit_price"] = df.groupby("product_id")["unit_price"].transform(
        lambda s: s.fillna(s.median())
    )
    df = df.dropna(subset=["unit_price"])
    df["line_revenue"] = df["quantity"] * df["unit_price"]
    return df


def run():
    # STEP 1: Extract
    customers, employees, orders, order_lines = extract()

    # STEP 2: Store original data in raw schema
    load_df(customers, "customers", "raw")
    load_df(employees, "employees", "raw")
    load_df(orders, "orders", "raw")
    load_df(order_lines, "order_lines", "raw")

    # STEP 3: Validate
    validate(customers, orders, order_lines)

    # STEP 4: Clean
    customers = clean_customers(customers)
    employees = clean_employees(employees)
    orders = clean_orders(orders)
    order_lines = clean_order_lines(order_lines)

    # STEP 5: Load cleaned data into staging
    load_df(customers, "stg_customers", "staging")
    load_df(employees, "stg_employees", "staging")
    load_df(orders, "stg_orders", "staging")
    load_df(order_lines, "stg_order_lines", "staging")

    print("Sales ETL complete.")


if __name__ == "__main__":
    run()
