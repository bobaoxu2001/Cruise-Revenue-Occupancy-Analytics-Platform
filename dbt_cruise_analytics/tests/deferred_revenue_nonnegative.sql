select
    sailing_id as entity_id,
    recognition_month as accounting_month,
    region,
    ship_class,
    deferred_revenue as failing_value
from {{ ref('mart_finance_revenue') }}
where deferred_revenue < 0

union all

select
    cast(accounting_month as varchar) || '-' || region || '-' || ship_class as entity_id,
    accounting_month,
    region,
    ship_class,
    least(beginning_deferred_revenue, ending_deferred_revenue) as failing_value
from {{ ref('mart_finance_revenue_waterfall_monthly') }}
where beginning_deferred_revenue < -0.01
   or ending_deferred_revenue < -0.01
