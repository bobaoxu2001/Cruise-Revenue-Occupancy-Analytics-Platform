select
    nullif(cast(sailing_id as varchar), '') as sailing_id,
    nullif(cast(ship_id as varchar), '') as ship_id,
    nullif(cast(itinerary_id as varchar), '') as itinerary_id,
    try_cast(nullif(cast(departure_date as varchar), '') as date) as departure_date,
    try_cast(nullif(cast(return_date as varchar), '') as date) as return_date,
    nullif(cast(sailing_status as varchar), '') as sailing_status
from {{ ref('sailings') }}
