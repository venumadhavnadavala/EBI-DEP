-- =========================================================
-- Enterprise BI Platform — Warehouse Schema
-- Layering: raw -> staging (loaded by ETL) -> marts (built by dbt)
-- This mirrors a real warehouse: never write transformed data
-- directly into raw. Keep raw immutable so you can always
-- re-run transformations without re-extracting from source.
-- =========================================================

CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS marts;

-- ---------- RAW (loaded as-is, minimal casting) ----------
CREATE TABLE IF NOT EXISTS raw.customers (
    customer_id     INT,
    customer_name   TEXT,
    email           TEXT,
    region          TEXT,
    signup_date     DATE,
    segment         TEXT
);

CREATE TABLE IF NOT EXISTS raw.employees (
    employee_id     INT,
    employee_name   TEXT,
    region          TEXT,
    hire_date       DATE,
    role            TEXT
);

CREATE TABLE IF NOT EXISTS raw.orders (
    order_id        INT,
    customer_id     INT,
    employee_id     INT,
    order_date      DATE,
    status          TEXT,
    region          TEXT
);

CREATE TABLE IF NOT EXISTS raw.order_lines (
    order_line_id   TEXT,
    order_id        INT,
    product_id      INT,
    quantity        INT,
    unit_price      NUMERIC
);

CREATE TABLE IF NOT EXISTS raw.suppliers (
    supplier_id         INT,
    supplier_name        TEXT,
    country              TEXT,
    reliability_score    NUMERIC
);

CREATE TABLE IF NOT EXISTS raw.products (
    product_id          INT,
    product_name        TEXT,
    category            TEXT,
    supplier_id         INT,
    unit_cost           NUMERIC,
    unit_price          NUMERIC,
    reorder_threshold   INT
);

CREATE TABLE IF NOT EXISTS raw.inventory_snapshots (
    product_id          INT,
    warehouse_region     TEXT,
    stock_on_hand        INT,
    last_restock_date    DATE,
    snapshot_date         DATE
);

CREATE TABLE IF NOT EXISTS raw.returns (
    return_id            INT,
    order_id              INT,
    product_id            INT,
    return_date           DATE,
    reason                TEXT,
    quantity_returned     INT
);

-- ---------- STAGING (cleaned, deduped, typed — written by ETL) ----------
CREATE TABLE IF NOT EXISTS staging.stg_customers (
    customer_id     INT PRIMARY KEY,
    customer_name   TEXT NOT NULL,
    email           TEXT,
    region          TEXT,
    signup_date     DATE,
    segment         TEXT
);

CREATE TABLE IF NOT EXISTS staging.stg_employees (
    employee_id     INT PRIMARY KEY,
    employee_name   TEXT,
    region          TEXT,
    hire_date       DATE,
    role            TEXT
);

CREATE TABLE IF NOT EXISTS staging.stg_orders (
    order_id        INT PRIMARY KEY,
    customer_id     INT,
    employee_id     INT,
    order_date      DATE,
    status          TEXT,
    region          TEXT
);

CREATE TABLE IF NOT EXISTS staging.stg_order_lines (
    order_line_id   TEXT PRIMARY KEY,
    order_id        INT,
    product_id      INT,
    quantity        INT,
    unit_price      NUMERIC,
    line_revenue    NUMERIC
);

CREATE TABLE IF NOT EXISTS staging.stg_products (
    product_id          INT PRIMARY KEY,
    product_name        TEXT,
    category             TEXT,
    supplier_id           INT,
    unit_cost             NUMERIC,
    unit_price             NUMERIC,
    reorder_threshold      INT
);

CREATE TABLE IF NOT EXISTS staging.stg_suppliers (
    supplier_id         INT PRIMARY KEY,
    supplier_name        TEXT,
    country               TEXT,
    reliability_score      NUMERIC
);

CREATE TABLE IF NOT EXISTS staging.stg_inventory (
    product_id           INT,
    warehouse_region      TEXT,
    stock_on_hand          INT,
    last_restock_date       DATE,
    snapshot_date            DATE,
    PRIMARY KEY (product_id, warehouse_region, snapshot_date)
);

CREATE TABLE IF NOT EXISTS staging.stg_returns (
    return_id             INT PRIMARY KEY,
    order_id               INT,
    product_id              INT,
    return_date               DATE,
    reason                     TEXT,
    quantity_returned            INT
);
