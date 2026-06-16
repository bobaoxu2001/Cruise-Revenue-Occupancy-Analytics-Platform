select
    date_day
from {{ ref('int_date_spine') }}
