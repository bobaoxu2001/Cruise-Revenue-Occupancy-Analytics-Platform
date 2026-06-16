with used_keys as (
    select distinct
        date_trunc('month', s.departure_date) as target_month,
        i.region,
        sh.ship_class
    from {{ ref('stg_sailings') }} s
    join {{ ref('stg_itineraries') }} i on s.itinerary_id = i.itinerary_id
    join {{ ref('stg_ships') }} sh on s.ship_id = sh.ship_id
),
targets as (
    select distinct target_month, region, ship_class
    from {{ ref('stg_aop_targets') }}
)
select used_keys.*
from used_keys
left join targets using (target_month, region, ship_class)
where targets.target_month is null
