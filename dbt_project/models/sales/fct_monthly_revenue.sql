-- MEMBER 1
-- KPI: Monthly revenue, order count, average order value, by region.
-- Only counts Completed orders — Cancelled/Pending orders don't
-- represent realized revenue. This exclusion is a business rule,
-- not a bug: be ready to justify it.

with orders as (
    select * from {{ source('staging', 'stg_orders') }}
    where status = 'Completed'
),

lines as (
    select * from {{ source('staging', 'stg_order_lines') }}
),

joined as (
    select
        o.order_id,
        o.region,
        date_trunc('month', o.order_date) as order_month,
        l.line_revenue
    from orders o
    join lines l on o.order_id = l.order_id
)

select
    order_month,
    region,
    count(distinct order_id)            as total_orders,
    sum(line_revenue)                    as total_revenue,
    round((sum(line_revenue) / nullif(count(distinct order_id), 0))::numeric, 2) as avg_order_value
from joined
group by 1, 2
order by 1, 2
