-- MEMBER 2
-- KPI: Return rate by product and by reason — used to flag
-- quality issues (high "Defective" rate) vs listing issues
-- (high "Wrong Item" rate).

with sold as (
    select product_id, sum(quantity) as units_sold
    from {{ source('staging', 'stg_order_lines') }} l
    join {{ source('staging', 'stg_orders') }} o on l.order_id = o.order_id
    where o.status = 'Completed'
    group by 1
),

returns_by_reason as (
    select
        product_id,
        reason,
        sum(quantity_returned) as units_returned
    from {{ source('staging', 'stg_returns') }}
    group by 1, 2
)

select
    p.product_id,
    p.product_name,
    r.reason,
    r.units_returned,
    s.units_sold,
    round(r.units_returned::numeric / nullif(s.units_sold, 0), 3) as return_rate
from returns_by_reason r
join {{ source('staging', 'stg_products') }} p on r.product_id = p.product_id
left join sold s on r.product_id = s.product_id
order by return_rate desc nulls last
