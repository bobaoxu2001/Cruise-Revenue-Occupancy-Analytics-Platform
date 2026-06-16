select
    coalesce(campaign_id, 'ORGANIC_OR_UNATTRIBUTED') as campaign_id,
    max(campaign_name) as campaign_name,
    coalesce(max(campaign_channel), 'Organic/Unattributed') as campaign_channel,
    coalesce(max(target_region), max(region)) as target_region,
    max(coalesce(spend, 0)) as campaign_spend,
    count(*) as attributed_bookings,
    sum(case when booking_status = 'cancelled' then 1 else 0 end) as cancelled_bookings,
    sum(net_booking_amount) as attributed_net_revenue,
    case
        when max(coalesce(spend, 0)) = 0 then null
        else sum(net_booking_amount) / max(spend)
    end as campaign_roas,
    case
        when count(*) = 0 then 0
        else sum(case when booking_status = 'cancelled' then 1 else 0 end) / count(*)
    end as cancellation_rate
from {{ ref('int_campaign_attribution') }}
group by 1
