select * from {{ ref('stg_reservations') }} where booking_status = 'cancelled' and cancellation_date is null
