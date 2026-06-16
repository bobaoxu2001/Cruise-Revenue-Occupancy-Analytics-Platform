select
    try_cast(nullif(cast(target_month as varchar), '') as date) as target_month,
    nullif(cast(region as varchar), '') as region,
    nullif(cast(ship_class as varchar), '') as ship_class,
    cast(revenue_target as double) as revenue_target,
    cast(occupancy_target as double) as occupancy_target,
    cast(booking_target as double) as booking_target
from {{ ref('aop_targets') }}
