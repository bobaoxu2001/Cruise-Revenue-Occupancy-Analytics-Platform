select
    nullif(cast(ship_id as varchar), '') as ship_id,
    nullif(cast(ship_name as varchar), '') as ship_name,
    nullif(cast(ship_class as varchar), '') as ship_class,
    cast(total_cabins as double) as total_cabins,
    cast(passenger_capacity as double) as passenger_capacity
from {{ ref('ships') }}
