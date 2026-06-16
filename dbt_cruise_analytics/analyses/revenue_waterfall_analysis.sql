select
    recognition_month,
    sum(cash_collected) as cash_collected,
    sum(recognized_revenue) as recognized_revenue,
    sum(deferred_revenue) as deferred_revenue,
    sum(refund_exposure) as refund_exposure,
    sum(cancellation_penalties) as cancellation_penalties
from {{ ref('mart_finance_revenue') }}
group by 1
order by 1
