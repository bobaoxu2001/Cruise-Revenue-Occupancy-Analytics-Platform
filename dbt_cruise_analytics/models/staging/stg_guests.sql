select
    nullif(cast(guest_id as varchar), '') as guest_id,
    nullif(cast(loyalty_tier as varchar), '') as loyalty_tier,
    nullif(cast(home_country as varchar), '') as home_country,
    nullif(cast(home_state as varchar), '') as home_state,
    nullif(cast(acquisition_channel as varchar), '') as acquisition_channel,
    try_cast(nullif(cast(first_booking_date as varchar), '') as date) as first_booking_date,
    nullif(cast(age_band as varchar), '') as age_band
from {{ ref('guests') }}
