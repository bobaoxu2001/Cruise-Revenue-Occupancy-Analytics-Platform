select p.*
from {{ ref('stg_payments') }} p
join {{ ref('stg_reservations') }} r on p.reservation_id = r.reservation_id
join {{ ref('stg_sailings') }} s on r.sailing_id = s.sailing_id
where p.payment_type = 'final_payment'
  and p.payment_date >= s.departure_date
