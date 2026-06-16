select
    s.sailing_id,
    s.departure_date,
    date_trunc('month', s.departure_date) as departure_month,
    s.region,
    s.itinerary_name,
    s.ship_class,
    s.passenger_capacity,
    s.available_passenger_nights,
    coalesce(sum(case when r.booking_status in ('completed', 'confirmed') then r.sold_passenger_nights else 0 end), 0) as sold_passenger_nights,
    coalesce(sum(case when r.booking_status in ('completed', 'confirmed') then r.net_booking_amount else 0 end), 0) as booked_net_revenue,
    coalesce(sum(case when r.booking_status = 'cancelled' then 1 else 0 end), 0) as cancelled_bookings,
    coalesce(sum(case when r.booking_status in ('completed', 'confirmed') then r.sold_passenger_nights else 0 end), 0) / nullif(s.available_passenger_nights, 0) as occupancy_rate,
    1 - (coalesce(sum(case when r.booking_status in ('completed', 'confirmed') then r.sold_passenger_nights else 0 end), 0) / nullif(s.available_passenger_nights, 0)) as occupancy_gap
from {{ ref('int_sailing_capacity') }} s
left join {{ ref('int_reservation_lifecycle') }} r on s.sailing_id = r.sailing_id
group by 1, 2, 3, 4, 5, 6, 7, 8
