select
    r.reservation_id,
    r.guest_id,
    r.sailing_id,
    r.cabin_id,
    r.booking_date,
    r.booking_status,
    r.cancellation_date,
    r.booking_channel,
    r.campaign_id,
    r.passenger_count,
    r.gross_booking_amount,
    r.discount_amount,
    r.net_booking_amount,
    r.currency,
    r.updated_at,
    s.departure_date,
    s.return_date,
    sc.region,
    sc.itinerary_name,
    sc.duration_days,
    sc.ship_class,
    date_diff('day', r.booking_date, s.departure_date) as booking_lead_days,
    case
        when r.booking_status = 'cancelled' then 1
        else 0
    end as is_cancelled,
    case
        when r.booking_status = 'completed' then 1
        else 0
    end as is_completed,
    r.passenger_count * sc.duration_days as sold_passenger_nights
from {{ ref('stg_reservations') }} r
join {{ ref('stg_sailings') }} s on r.sailing_id = s.sailing_id
join {{ ref('int_sailing_capacity') }} sc on r.sailing_id = sc.sailing_id
