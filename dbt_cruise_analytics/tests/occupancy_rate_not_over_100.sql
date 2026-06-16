select *
from {{ ref('fct_occupancy_daily') }}
where occupancy_rate > 1.0001
