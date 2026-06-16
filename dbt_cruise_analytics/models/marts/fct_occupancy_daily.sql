with reservation_nights as (
    select
        d.date_day,
        r.sailing_id,
        r.region,
        r.ship_class,
        sum(r.passenger_count) as sold_passengers
    from {{ ref('int_reservation_lifecycle') }} r
    join {{ ref('int_date_spine') }} d
      on d.date_day >= r.departure_date
     and d.date_day < r.return_date
    where r.booking_status in ('completed', 'confirmed')
    group by 1, 2, 3, 4
),
sailing_days as (
    select
        d.date_day,
        sc.sailing_id,
        sc.region,
        sc.ship_class,
        sc.passenger_capacity
    from {{ ref('int_sailing_capacity') }} sc
    join {{ ref('int_date_spine') }} d
      on d.date_day >= sc.departure_date
     and d.date_day < sc.return_date
)
select
    sd.date_day,
    date_trunc('month', sd.date_day) as month_start,
    sd.sailing_id,
    sd.region,
    sd.ship_class,
    coalesce(rn.sold_passengers, 0) as sold_passengers,
    sd.passenger_capacity as available_passengers,
    coalesce(rn.sold_passengers, 0) as sold_passenger_nights,
    sd.passenger_capacity as available_passenger_nights,
    case
        when sd.passenger_capacity = 0 then 0
        else coalesce(rn.sold_passengers, 0) / sd.passenger_capacity
    end as occupancy_rate
from sailing_days sd
left join reservation_nights rn
  on sd.date_day = rn.date_day
 and sd.sailing_id = rn.sailing_id
