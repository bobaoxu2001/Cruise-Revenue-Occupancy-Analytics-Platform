select *
from {{ ref('fct_revenue_recognition') }}
where recognized_revenue < 0
