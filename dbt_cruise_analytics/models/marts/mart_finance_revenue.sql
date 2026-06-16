with cash_by_sailing as (
    select
        r.sailing_id,
        sum(case when p.payment_type in ('deposit', 'final_payment') then p.payment_amount else 0 end) as cash_collected,
        sum(case when p.payment_type = 'refund' then p.payment_amount else 0 end) as refund_amount,
        sum(case when p.payment_type = 'cancellation_penalty' then p.payment_amount else 0 end) as cancellation_penalties
    from {{ ref('int_reservation_lifecycle') }} r
    join {{ ref('stg_payments') }} p on r.reservation_id = p.reservation_id
    group by 1
),
recognized as (
    select
        sailing_id,
        sum(recognized_revenue) as recognized_revenue
    from {{ ref('fct_revenue_recognition') }}
    group by 1
)
select
    s.sailing_id,
    s.return_date as recognition_date,
    date_trunc('month', s.return_date) as recognition_month,
    s.region,
    s.ship_class,
    coalesce(c.cash_collected, 0) as cash_collected,
    coalesce(r.recognized_revenue, 0) as recognized_revenue,
    greatest(coalesce(c.cash_collected, 0) - coalesce(r.recognized_revenue, 0), 0) as deferred_revenue,
    abs(coalesce(c.refund_amount, 0)) as refund_exposure,
    coalesce(c.cancellation_penalties, 0) as cancellation_penalties
from {{ ref('int_sailing_capacity') }} s
left join cash_by_sailing c on s.sailing_id = c.sailing_id
left join recognized r on s.sailing_id = r.sailing_id
