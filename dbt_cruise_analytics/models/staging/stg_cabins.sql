select
    nullif(cast(cabin_id as varchar), '') as cabin_id,
    nullif(cast(ship_id as varchar), '') as ship_id,
    nullif(cast(cabin_category as varchar), '') as cabin_category,
    cast(deck as double) as deck,
    cast(capacity as double) as capacity,
    cast(list_price_multiplier as double) as list_price_multiplier
from {{ ref('cabins') }}
