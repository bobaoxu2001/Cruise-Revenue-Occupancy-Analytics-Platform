select *
from {{ ref('mart_executive_scorecard') }}
where revenue_target <= 0
   or occupancy_target <= 0
   or booking_target <= 0
