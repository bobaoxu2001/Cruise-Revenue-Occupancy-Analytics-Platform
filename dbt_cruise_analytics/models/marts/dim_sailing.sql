select
    sc.*,
    s.sailing_status
from {{ ref('int_sailing_capacity') }} sc
join {{ ref('stg_sailings') }} s on sc.sailing_id = s.sailing_id
