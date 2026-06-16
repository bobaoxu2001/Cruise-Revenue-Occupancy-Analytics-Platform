select
    nullif(cast(reservation_id as varchar), '') as reservation_id,
    nullif(cast(guest_id as varchar), '') as guest_id,
    nullif(cast(sailing_id as varchar), '') as sailing_id,
    nullif(cast(cabin_id as varchar), '') as cabin_id,
    try_cast(nullif(cast(booking_date as varchar), '') as date) as booking_date,
    nullif(cast(booking_status as varchar), '') as booking_status,
    try_cast(nullif(cast(cancellation_date as varchar), '') as date) as cancellation_date,
    nullif(cast(booking_channel as varchar), '') as booking_channel,
    nullif(cast(campaign_id as varchar), '') as campaign_id,
    cast(passenger_count as double) as passenger_count,
    cast(gross_booking_amount as double) as gross_booking_amount,
    cast(discount_amount as double) as discount_amount,
    cast(net_booking_amount as double) as net_booking_amount,
    nullif(cast(currency as varchar), '') as currency,
    try_cast(nullif(cast(updated_at as varchar), '') as date) as updated_at
from {{ ref('reservations') }}
