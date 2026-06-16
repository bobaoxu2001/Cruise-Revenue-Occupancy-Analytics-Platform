with payment_activity as (
    select
        payment_month as accounting_month,
        region,
        ship_class,
        sum(case when payment_type in ('deposit', 'final_payment') then payment_amount else 0 end) as cash_collected,
        -- Refund payment rows are stored as negative amounts. Keeping the
        -- signed value makes the deferred revenue roll-forward auditable.
        sum(case when payment_type = 'refund' then payment_amount else 0 end) as refunds,
        sum(case when payment_type = 'cancellation_penalty' then payment_amount else 0 end) as cancellation_penalties
    from {{ ref('int_payment_events') }}
    group by 1, 2, 3
),
recognized_activity as (
    select
        recognition_month as accounting_month,
        region,
        ship_class,
        sum(recognized_revenue) as recognized_revenue
    from {{ ref('fct_revenue_recognition') }}
    group by 1, 2, 3
),
reporting_keys as (
    select accounting_month, region, ship_class from payment_activity
    union
    select accounting_month, region, ship_class from recognized_activity
    union
    select target_month as accounting_month, region, ship_class from {{ ref('stg_aop_targets') }}
),
monthly_activity as (
    select
        k.accounting_month,
        k.region,
        k.ship_class,
        coalesce(p.cash_collected, 0) as cash_collected,
        coalesce(p.refunds, 0) as refunds,
        coalesce(p.cancellation_penalties, 0) as cancellation_penalties,
        coalesce(r.recognized_revenue, 0) as recognized_revenue,
        coalesce(p.cash_collected, 0)
            + coalesce(p.cancellation_penalties, 0)
            + coalesce(p.refunds, 0) as net_cash_activity
    from reporting_keys k
    left join payment_activity p
      on k.accounting_month = p.accounting_month
     and k.region = p.region
     and k.ship_class = p.ship_class
    left join recognized_activity r
      on k.accounting_month = r.accounting_month
     and k.region = r.region
     and k.ship_class = r.ship_class
),
waterfall as (
    select
        *,
        sum(net_cash_activity - recognized_revenue) over (
            partition by region, ship_class
            order by accounting_month
            rows between unbounded preceding and current row
        ) as ending_deferred_revenue
    from monthly_activity
),
final as (
    select
        accounting_month,
        region,
        ship_class,
        ending_deferred_revenue - (net_cash_activity - recognized_revenue) as beginning_deferred_revenue,
        cash_collected,
        refunds,
        cancellation_penalties,
        recognized_revenue,
        ending_deferred_revenue,
        net_cash_activity
    from waterfall
)
select
    accounting_month,
    region,
    ship_class,
    beginning_deferred_revenue,
    cash_collected,
    refunds,
    cancellation_penalties,
    recognized_revenue,
    ending_deferred_revenue,
    net_cash_activity,
    case
        when beginning_deferred_revenue + net_cash_activity = 0 then 0
        else recognized_revenue / nullif(beginning_deferred_revenue + net_cash_activity, 0)
    end as revenue_recognition_rate
from final
