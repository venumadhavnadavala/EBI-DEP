-- MEMBER 1
-- KPI: Revenue and order volume attributed to each employee (sales rep).

with completed_orders as (
    select * from {{ source('staging', 'stg_orders') }}
    where status = 'Completed'
),

lines as (
    select * from {{ source('staging', 'stg_order_lines') }}
),

emp_orders as (
    select
        o.employee_id,
        o.order_id,
        l.line_revenue
    from completed_orders o
    join lines l on o.order_id = l.order_id
)

select
    e.employee_id,
    e.employee_name,
    e.region,
    e.role,
    count(distinct eo.order_id)   as orders_closed,
    coalesce(sum(eo.line_revenue), 0) as revenue_generated
from {{ source('staging', 'stg_employees') }} e
left join emp_orders eo on e.employee_id = eo.employee_id
group by 1, 2, 3, 4
order by revenue_generated desc
