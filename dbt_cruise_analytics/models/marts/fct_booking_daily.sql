{{
    config(
        materialized='incremental',
        unique_key=[
            'booking_date',
            'departure_date',
            'region',
            'ship_class',
            'booking_channel',
            'lead_time_bucket'
        ],
        incremental_strategy='delete+insert'
    )
}}

-- Production pattern: dbt-duckdb uses delete+insert locally, while a
-- Snowflake target can compile the same unique grain into MERGE semantics.
-- The incremental filter reprocesses only booking dates at or after the
-- current max loaded booking_date, which keeps late-arriving same-day updates
-- in scope without rebuilding the entire fact.
with booking_source as (
    select *
    from {{ ref('int_booking_lead_time') }}

    {% if is_incremental() %}
        where booking_date >= (
            select coalesce(max(booking_date), date '1900-01-01')
            from {{ this }}
        )
    {% endif %}
)

select
    booking_date,
    date_trunc('month', booking_date) as booking_month,
    departure_date,
    date_trunc('month', departure_date) as departure_month,
    region,
    ship_class,
    booking_channel,
    lead_time_bucket,
    count(*) as bookings,
    sum(case when booking_status = 'cancelled' then 1 else 0 end) as cancellations,
    sum(passenger_count) as booked_passengers,
    sum(gross_booking_amount) as gross_booking_revenue,
    sum(net_booking_amount) as net_booking_revenue
from booking_source
group by 1, 2, 3, 4, 5, 6, 7, 8
