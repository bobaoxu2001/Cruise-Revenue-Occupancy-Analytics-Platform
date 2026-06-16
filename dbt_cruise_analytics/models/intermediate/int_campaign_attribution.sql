select
    r.reservation_id,
    r.campaign_id,
    c.channel as campaign_channel,
    c.campaign_name,
    c.target_region,
    c.spend,
    r.booking_channel,
    r.region,
    r.net_booking_amount,
    r.booking_status,
    r.is_cancelled,
    r.passenger_count
from {{ ref('int_reservation_lifecycle') }} r
left join {{ ref('stg_marketing_campaigns') }} c on r.campaign_id = c.campaign_id
