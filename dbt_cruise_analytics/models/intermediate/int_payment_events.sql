select
    p.payment_id,
    p.reservation_id,
    r.sailing_id,
    p.payment_type,
    p.payment_date,
    date_trunc('month', p.payment_date) as payment_month,
    p.payment_amount,
    p.payment_status,
    r.booking_status,
    r.departure_date,
    r.return_date,
    r.region,
    r.ship_class
from {{ ref('stg_payments') }} p
join {{ ref('int_reservation_lifecycle') }} r on p.reservation_id = r.reservation_id
