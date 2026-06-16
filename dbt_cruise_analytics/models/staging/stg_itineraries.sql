select
    nullif(cast(itinerary_id as varchar), '') as itinerary_id,
    nullif(cast(region as varchar), '') as region,
    nullif(cast(itinerary_name as varchar), '') as itinerary_name,
    nullif(cast(embark_port as varchar), '') as embark_port,
    nullif(cast(disembark_port as varchar), '') as disembark_port,
    cast(duration_days as double) as duration_days,
    cast(base_price_multiplier as double) as base_price_multiplier
from {{ ref('itineraries') }}
