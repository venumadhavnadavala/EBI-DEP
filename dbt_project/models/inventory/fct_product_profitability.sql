-- MEMBER 2
-- KPI: Margin and profitability per product, adjusted for returns.
-- Gross margin = (price - cost) / price.
-- Net units = units sold - units returned, since returned goods
-- don't generate realized profit.

with sold as (
    select
        l.product_id,
        sum(l.quantity) as units_sold,
        sum(l.line_revenue) as gross_revenue
    from {{ source('staging', 'stg_order_lines') }} l
    join {{ source('staging', 'stg_orders') }} o on l.order_id = o.order_id
    where o.status = 'Completed'
    group by 1
),

returned as (
    select
        product_id,
        sum(quantity_returned) as units_returned
    from {{ source('staging', 'stg_returns') }}
    group by 1
)

select
    p.product_id,
    p.product_name,
    p.category,
    p.unit_cost,
    p.unit_price,
    round(((p.unit_price - p.unit_cost) / nullif(p.unit_price, 0))::numeric, 3) as gross_margin_pct,
    coalesce(s.units_sold, 0)                                          as units_sold,
    coalesce(r.units_returned, 0)                                       as units_returned,
    coalesce(s.units_sold, 0) - coalesce(r.units_returned, 0)            as net_units_sold,
    coalesce(s.gross_revenue, 0)                                          as gross_revenue,
    round(
        ((coalesce(s.units_sold, 0) - coalesce(r.units_returned, 0)) * (p.unit_price - p.unit_cost))::numeric,
        2
    )                                                                       as estimated_net_profit
from {{ source('staging', 'stg_products') }} p
left join sold s on p.product_id = s.product_id
left join returned r on p.product_id = r.product_id
