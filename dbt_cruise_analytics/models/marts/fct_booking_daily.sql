select
    booking_date,
    date_trunc('month', booking_date) as booking_month,
    departure_date,
    date_trunc('month', departure_date) as departure_month,
    region,
    ship_class,
    booking_channel,
    lead_time_bucket,
    count(*) as bookings,
    sum(case when booking_status = 'cancelled' then 1 else 0 end) as cancellations,
    sum(passenger_count) as booked_passengers,
    sum(gross_booking_amount) as gross_booking_revenue,
    sum(net_booking_amount) as net_booking_revenue
from {{ ref('int_booking_lead_time') }}
group by 1, 2, 3, 4, 5, 6, 7, 8
