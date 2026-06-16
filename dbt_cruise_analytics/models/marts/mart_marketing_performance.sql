select
    campaign_id,
    campaign_name,
    campaign_channel,
    target_region,
    campaign_spend,
    attributed_bookings,
    cancelled_bookings,
    attributed_net_revenue,
    campaign_roas,
    cancellation_rate,
    attributed_net_revenue - campaign_spend as contribution_after_media
from {{ ref('fct_campaign_performance') }}
