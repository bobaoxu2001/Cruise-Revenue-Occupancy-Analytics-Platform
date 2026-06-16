select
    s.sailing_id,
    s.ship_id,
    s.itinerary_id,
    s.departure_date,
    s.return_date,
    i.region,
    i.itinerary_name,
    i.duration_days,
    sh.ship_class,
    sh.passenger_capacity,
    sh.passenger_capacity * i.duration_days as available_passenger_nights
from {{ ref('stg_sailings') }} s
join {{ ref('stg_ships') }} sh on s.ship_id = sh.ship_id
join {{ ref('stg_itineraries') }} i on s.itinerary_id = i.itinerary_id
