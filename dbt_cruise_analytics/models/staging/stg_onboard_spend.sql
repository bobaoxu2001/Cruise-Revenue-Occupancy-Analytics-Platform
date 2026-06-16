select
    nullif(cast(onboard_spend_id as varchar), '') as onboard_spend_id,
    nullif(cast(reservation_id as varchar), '') as reservation_id,
    nullif(cast(service_category as varchar), '') as service_category,
    cast(spend_amount as double) as spend_amount,
    try_cast(nullif(cast(spend_date as varchar), '') as date) as spend_date
from {{ ref('onboard_spend') }}
