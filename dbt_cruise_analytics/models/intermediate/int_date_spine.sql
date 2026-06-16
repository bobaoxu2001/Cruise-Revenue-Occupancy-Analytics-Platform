with bounds as (
    select
        min(departure_date) as min_date,
        max(return_date) as max_date
    from {{ ref('stg_sailings') }}
),
spine as (
    select cast(date_day as date) as date_day
    from bounds,
    generate_series(min_date, max_date, interval 1 day) as t(date_day)
)
select
    date_day,
    date_trunc('month', date_day) as month_start,
    extract(year from date_day) as year_number,
    extract(month from date_day) as month_number,
    extract(dayofweek from date_day) as day_of_week
from spine
