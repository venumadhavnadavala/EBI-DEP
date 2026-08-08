"""
MEMBER 2 — Product & Inventory Analytics ETL
Owns: products, suppliers, inventory_snapshots, returns (raw -> staging)

Pipeline stages:

1. EXTRACT   — Read source CSV files
2. LOAD RAW  — Store original data in raw schema
3. VALIDATE  — Check data quality
4. CLEAN     — Remove duplicates, fix nulls, convert types
5. TRANSFORM — Prepare inventory data for analytics
6. LOAD      — Store cleaned data in staging schema — same pattern, different domain. That symmetry is the
   whole point: it's what lets both of you say "we both built ETL, SQL,
   Airflow, dbt, FastAPI, dashboards" truthfully in an interview.
"""

import pandas as pd
from db import load_df

RAW = "data/raw"


def extract():
    products = pd.read_csv(f"{RAW}/products.csv")
    suppliers = pd.read_csv(f"{RAW}/suppliers.csv")
    inventory = pd.read_csv(f"{RAW}/inventory_snapshots.csv")
    returns = pd.read_csv(f"{RAW}/returns.csv")
    return products, suppliers, inventory, returns


def validate(products, inventory):
    issues = []

    if products.empty:
        issues.append("products: dataset is empty")

    if inventory.empty:
        issues.append("inventory: dataset is empty")

    if not inventory["product_id"].isin(products["product_id"]).all():
        issues.append("inventory: product_id not found in products")

    if (products["unit_cost"] > products["unit_price"]).any():
        issues.append(
            "products: unit_cost exceeds unit_price on some rows (margin < 0)"
        )

    if products["product_id"].isna().any():
        issues.append("products: missing product_id values found")

    if inventory["product_id"].isna().any():
        issues.append("inventory: missing product_id values found")

    if issues:
        print("VALIDATION WARNINGS:")
        for i in issues:
            print(" -", i)

    return issues


def clean_products(products: pd.DataFrame) -> pd.DataFrame:
    df = products.drop_duplicates(subset=["product_id"]).copy()

    df["unit_cost"] = pd.to_numeric(df["unit_cost"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    df["unit_cost"] = df["unit_cost"].fillna(df["unit_cost"].median())
    df["unit_price"] = df["unit_price"].fillna(df["unit_price"].median())

    return df


def clean_suppliers(suppliers: pd.DataFrame) -> pd.DataFrame:
    return suppliers.drop_duplicates(subset=["supplier_id"]).copy()


def clean_inventory(inventory: pd.DataFrame) -> pd.DataFrame:
    df = inventory.drop_duplicates(
        subset=["product_id", "warehouse_region", "snapshot_date"]
    ).copy()

    df["last_restock_date"] = pd.to_datetime(
        df["last_restock_date"],
        errors="coerce"
    )

    df["snapshot_date"] = pd.to_datetime(
        df["snapshot_date"],
        errors="coerce"
    )

    df["stock_on_hand"] = pd.to_numeric(
        df["stock_on_hand"],
        errors="coerce"
    )

    # Make sure negative stock values don't make it into staging.
    df["stock_on_hand"] = df["stock_on_hand"].clip(lower=0)

    return df


def clean_returns(returns: pd.DataFrame) -> pd.DataFrame:
    df = returns.drop_duplicates(subset=["return_id"]).copy()

    df["return_date"] = pd.to_datetime(
        df["return_date"],
        errors="coerce"
    )

    df["quantity_returned"] = pd.to_numeric(
        df["quantity_returned"],
        errors="coerce"
    )

    df = df.dropna(subset=["return_date"])

    df["quantity_returned"] = df["quantity_returned"].clip(lower=1)

    return df


def run():
    # STEP 1: Extract
    products, suppliers, inventory, returns = extract()

    # STEP 2: Store original data in raw schema
    load_df(products, "products", "raw")
    load_df(suppliers, "suppliers", "raw")
    load_df(inventory, "inventory_snapshots", "raw")
    load_df(returns, "returns", "raw")

    # STEP 3: Validate
    validate(products, inventory)

    # STEP 4: Clean
    products = clean_products(products)
    suppliers = clean_suppliers(suppliers)
    inventory = clean_inventory(inventory)
    returns = clean_returns(returns)

    # STEP 5: Load cleaned data into staging
    load_df(products, "stg_products", "staging")
    load_df(suppliers, "stg_suppliers", "staging")
    load_df(inventory, "stg_inventory", "staging")
    load_df(returns, "stg_returns", "staging")

    print("Inventory ETL complete.")


if __name__ == "__main__":
    run()