select *
from {{ ref('fct_occupancy_daily') }}
where occupancy_rate < -0.0001
