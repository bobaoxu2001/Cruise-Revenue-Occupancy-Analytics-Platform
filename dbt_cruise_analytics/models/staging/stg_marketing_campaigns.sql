select
    nullif(cast(campaign_id as varchar), '') as campaign_id,
    nullif(cast(channel as varchar), '') as channel,
    nullif(cast(campaign_name as varchar), '') as campaign_name,
    try_cast(nullif(cast(start_date as varchar), '') as date) as start_date,
    try_cast(nullif(cast(end_date as varchar), '') as date) as end_date,
    cast(spend as double) as spend,
    nullif(cast(target_region as varchar), '') as target_region
from {{ ref('marketing_campaigns') }}
