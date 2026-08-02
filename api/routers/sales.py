"""
MEMBER 1 — Sales & Customer API
Endpoints read from marts.fct_* tables built by dbt. This router
does NOT run business logic — that lives in SQL/dbt. The API layer's
job is just to parameterize, paginate, and serialize. Know that
separation; it's a common interview question ("why isn't this logic
in Python?").
"""
from fastapi import APIRouter, Query
from db import query

router = APIRouter(prefix="/sales", tags=["sales"])


@router.get("/revenue/monthly")
def monthly_revenue(region: str | None = None):
    sql = "select * from marts.fct_monthly_revenue"
    params = {}
    if region:
        sql += " where region = :region"
        params["region"] = region
    sql += " order by order_month"
    return query(sql, params)


@router.get("/customers/top")
def top_customers(limit: int = Query(10, le=100)):
    sql = """
        select customer_id, customer_name, region, segment,
               total_orders, lifetime_value, at_risk_flag
        from marts.fct_customer_ltv
        order by lifetime_value desc
        limit :limit
    """
    return query(sql, {"limit": limit})


@router.get("/customers/at-risk")
def at_risk_customers():
    sql = """
        select customer_id, customer_name, region, lifetime_value,
               days_since_last_order
        from marts.fct_customer_ltv
        where at_risk_flag = true
        order by lifetime_value desc
    """
    return query(sql)


@router.get("/employees/performance")
def salesperson_performance():
    sql = "select * from marts.fct_salesperson_performance order by revenue_generated desc"
    return query(sql)


@router.get("/kpis/summary")
def sales_kpi_summary():
    sql = """
        select
            sum(total_revenue) as total_revenue,
            sum(total_orders)   as total_orders,
            round(avg(avg_order_value), 2) as avg_order_value
        from marts.fct_monthly_revenue
    """
    rows = query(sql)
    return rows[0] if rows else {}
