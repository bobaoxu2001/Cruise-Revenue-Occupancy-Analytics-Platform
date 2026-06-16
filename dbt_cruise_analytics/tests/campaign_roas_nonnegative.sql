select *
from {{ ref('mart_marketing_performance') }}
where campaign_roas < 0
