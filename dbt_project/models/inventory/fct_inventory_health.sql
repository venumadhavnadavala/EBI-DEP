-- MEMBER 2
-- KPI: Inventory health per product — current stock vs reorder
-- threshold, and a rough turnover estimate using trailing sales
-- volume from the sales staging table (this is the one place the
-- two domains genuinely intersect — know this join cold).

with latest_snapshot as (
    select distinct on (product_id, warehouse_region)
        product_id, warehouse_region, stock_on_hand, snapshot_date
    from {{ source('staging', 'stg_inventory') }}
    order by product_id, warehouse_region, snapshot_date desc
),

sales_last_90d as (
    select
        l.product_id,
        sum(l.quantity) as units_sold_90d
    from {{ source('staging', 'stg_order_lines') }} l
    join {{ source('staging', 'stg_orders') }} o on l.order_id = o.order_id
    where o.status = 'Completed'
      and o.order_date >= current_date - interval '90 days'
    group by 1
)

select
    p.product_id,
    p.product_name,
    p.category,
    ls.warehouse_region,
    coalesce(ls.stock_on_hand, 0)   as stock_on_hand,
    p.reorder_threshold,
    coalesce(s.units_sold_90d, 0)    as units_sold_90d,
    round(coalesce(s.units_sold_90d, 0) / 90.0, 2) as avg_daily_sales,
    case
        when coalesce(ls.stock_on_hand, 0) <= p.reorder_threshold then true
        else false
    end                                                  as needs_reorder,
    case
        when coalesce(s.units_sold_90d, 0) / 90.0 > 0
        then round(coalesce(ls.stock_on_hand, 0) / (s.units_sold_90d / 90.0), 1)
        else null
    end                                                   as days_of_stock_remaining
from {{ source('staging', 'stg_products') }} p
left join latest_snapshot ls on p.product_id = ls.product_id
left join sales_last_90d s on p.product_id = s.product_id
