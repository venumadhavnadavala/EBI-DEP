from sqlalchemy import text

from api.db import SessionLocal


def get_monthly_revenue():
    db = SessionLocal()

    try:
        result = db.execute(
            text("""
                SELECT
                    order_month,
                    region,
                    total_orders,
                    total_revenue,
                    avg_order_value
                FROM marts.fct_monthly_revenue
                ORDER BY order_month, region
            """)
        )

        return [dict(row._mapping) for row in result]

    finally:
        db.close()