-- Snowflake recursive CTE date spine for sailing analytics.
with recursive date_spine(date_day) as (
    select to_date('2024-01-01')
    union all
    select dateadd(day, 1, date_day)
    from date_spine
    where date_day < to_date('2026-12-31')
)
select
    date_day,
    date_trunc('month', date_day) as month_start,
    year(date_day) as year_number,
    month(date_day) as month_number
from date_spine;
