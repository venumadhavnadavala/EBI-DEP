-- MEMBER 1
-- KPI: Customer Lifetime Value (CLV) — total realized revenue per
-- customer since signup, plus order frequency and recency.
-- Recency = days since last order; used downstream by the AI
-- insight layer to flag "at risk" customers (no order in 90+ days).

with completed_orders as (
    select * from {{ source('staging', 'stg_orders') }}
    where status = 'Completed'
),

lines as (
    select * from {{ source('staging', 'stg_order_lines') }}
),

customer_orders as (
    select
        o.customer_id,
        o.order_id,
        o.order_date,
        l.line_revenue
    from completed_orders o
    join lines l on o.order_id = l.order_id
),

agg as (
    select
        customer_id,
        count(distinct order_id)         as total_orders,
        sum(line_revenue)                 as lifetime_value,
        max(order_date)                    as last_order_date,
        (current_date - max(order_date)::date) as days_since_last_order
    from customer_orders
    group by 1
)

select
    c.customer_id,
    c.customer_name,
    c.region,
    c.segment,
    coalesce(a.total_orders, 0)          as total_orders,
    coalesce(a.lifetime_value, 0)         as lifetime_value,
    a.last_order_date,
    a.days_since_last_order,
    case
        when a.days_since_last_order > 90 then true
        else false
    end                                     as at_risk_flag
from {{ source('staging', 'stg_customers') }} c
left join agg a on c.customer_id = a.customer_id
