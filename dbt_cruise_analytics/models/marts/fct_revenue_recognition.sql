select
    recognition_date,
    recognition_month,
    sailing_id,
    region,
    ship_class,
    sum(recognized_revenue) as recognized_revenue,
    sum(cash_collected) as cash_collected,
    sum(refunds) as refunds,
    sum(cancellation_penalties) as cancellation_penalties,
    sum(sold_passenger_nights) as sold_passenger_nights,
    case
        when sum(sold_passenger_nights) = 0 then 0
        else sum(recognized_revenue) / sum(sold_passenger_nights)
    end as revenue_per_passenger_night
from {{ ref('int_revenue_events') }}
group by 1, 2, 3, 4, 5
