select
    reservation_id,
    sailing_id,
    booking_date,
    departure_date,
    region,
    ship_class,
    booking_channel,
    booking_status,
    passenger_count,
    gross_booking_amount,
    net_booking_amount,
    booking_lead_days,
    case
        when booking_lead_days >= 180 then '180+ days'
        when booking_lead_days >= 120 then '120-179 days'
        when booking_lead_days >= 90 then '90-119 days'
        when booking_lead_days >= 60 then '60-89 days'
        when booking_lead_days >= 30 then '30-59 days'
        else '0-29 days'
    end as lead_time_bucket
from {{ ref('int_reservation_lifecycle') }}
