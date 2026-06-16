with reservation_revenue as (
    select
        reservation_id,
        sailing_id,
        return_date as recognition_date,
        date_trunc('month', return_date) as recognition_month,
        region,
        ship_class,
        net_booking_amount as recognized_revenue,
        sold_passenger_nights
    from {{ ref('int_reservation_lifecycle') }}
    where booking_status = 'completed'
),
cash as (
    select
        reservation_id,
        sum(case when payment_type in ('deposit', 'final_payment') then payment_amount else 0 end) as cash_collected,
        sum(case when payment_type = 'refund' then payment_amount else 0 end) as refunds,
        sum(case when payment_type = 'cancellation_penalty' then payment_amount else 0 end) as cancellation_penalties
    from {{ ref('int_payment_events') }}
    group by 1
)
select
    rr.*,
    coalesce(c.cash_collected, 0) as cash_collected,
    coalesce(c.refunds, 0) as refunds,
    coalesce(c.cancellation_penalties, 0) as cancellation_penalties
from reservation_revenue rr
left join cash c on rr.reservation_id = c.reservation_id
