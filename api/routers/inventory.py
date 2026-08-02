"""
MEMBER 2 — Product & Inventory API
Same pattern as sales.py: thin router, business logic lives in dbt marts.
"""
from fastapi import APIRouter, Query
from db import query

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/health")
def inventory_health(needs_reorder: bool | None = None):
    sql = "select * from marts.fct_inventory_health"
    params = {}
    if needs_reorder is not None:
        sql += " where needs_reorder = :needs_reorder"
        params["needs_reorder"] = needs_reorder
    sql += " order by days_of_stock_remaining nulls last"
    return query(sql, params)


@router.get("/profitability/top")
def top_profitable_products(limit: int = Query(10, le=100)):
    sql = """
        select product_id, product_name, category, gross_margin_pct,
               net_units_sold, estimated_net_profit
        from marts.fct_product_profitability
        order by estimated_net_profit desc
        limit :limit
    """
    return query(sql, {"limit": limit})


@router.get("/returns/analysis")
def return_analysis(min_rate: float = 0.0):
    sql = """
        select product_id, product_name, reason, units_returned,
               units_sold, return_rate
        from marts.fct_return_analysis
        where return_rate >= :min_rate
        order by return_rate desc
    """
    return query(sql, {"min_rate": min_rate})


@router.get("/forecast/reorder-needed")
def reorder_needed():
    sql = """
        select product_id, product_name, category, stock_on_hand,
               reorder_threshold, avg_daily_sales, days_of_stock_remaining
        from marts.fct_inventory_health
        where needs_reorder = true
        order by days_of_stock_remaining nulls first
    """
    return query(sql)


@router.get("/kpis/summary")
def inventory_kpi_summary():
    sql = """
        select
            count(*) filter (where needs_reorder) as products_needing_reorder,
            round(avg(gross_margin_pct), 3)          as avg_margin
        from marts.fct_inventory_health h
        join marts.fct_product_profitability p using (product_id)
    """
    rows = query(sql)
    return rows[0] if rows else {}
