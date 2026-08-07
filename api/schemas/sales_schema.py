from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class MonthlyRevenueResponse(BaseModel):
    order_month: datetime
    region: str
    total_orders: int
    total_revenue: Decimal
    avg_order_value: Decimal

    class Config:
        from_attributes = True