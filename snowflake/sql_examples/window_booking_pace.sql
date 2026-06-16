-- Booking pace curve using Snowflake window functions.
select
    sailing_id,
    booking_date,
    datediff(day, booking_date, departure_date) as lead_days,
    sum(net_booking_amount) over (
        partition by sailing_id
        order by booking_date
        rows between unbounded preceding and current row
    ) as cumulative_booked_revenue,
    sum(passenger_count) over (
        partition by sailing_id
        order by booking_date
        rows between unbounded preceding and current row
    ) as cumulative_booked_passengers
from analytics.int_reservation_lifecycle
where booking_status <> 'cancelled';
