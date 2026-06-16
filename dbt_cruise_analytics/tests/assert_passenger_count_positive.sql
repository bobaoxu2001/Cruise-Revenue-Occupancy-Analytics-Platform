select * from {{ ref('stg_reservations') }} where passenger_count <= 0
