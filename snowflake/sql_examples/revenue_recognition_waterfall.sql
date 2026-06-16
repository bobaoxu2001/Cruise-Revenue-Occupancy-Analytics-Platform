-- Revenue recognition waterfall: cash collected, refunds, deferred, recognized.
select
    date_trunc('month', recognition_date) as recognition_month,
    sum(cash_collected) as cash_collected,
    sum(refund_exposure) as refund_exposure,
    sum(cancellation_penalties) as cancellation_penalties,
    sum(recognized_revenue) as recognized_revenue,
    sum(deferred_revenue) as ending_deferred_revenue
from analytics.mart_finance_revenue
group by 1
order by 1;
