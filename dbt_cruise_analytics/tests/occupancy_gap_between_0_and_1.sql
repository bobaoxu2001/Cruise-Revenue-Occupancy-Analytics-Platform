select *
from {{ ref('mart_revenue_management') }}
where occupancy_gap < -0.0001
   or occupancy_gap > 1.0001
