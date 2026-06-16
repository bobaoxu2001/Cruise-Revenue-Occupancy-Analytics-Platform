select
    nullif(cast(payment_id as varchar), '') as payment_id,
    nullif(cast(reservation_id as varchar), '') as reservation_id,
    nullif(cast(payment_type as varchar), '') as payment_type,
    try_cast(nullif(cast(payment_date as varchar), '') as date) as payment_date,
    cast(payment_amount as double) as payment_amount,
    nullif(cast(payment_status as varchar), '') as payment_status
from {{ ref('payments') }}
