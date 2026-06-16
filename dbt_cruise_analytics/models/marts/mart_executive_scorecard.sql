with revenue as (
    select
        recognition_month as month_start,
        region,
        ship_class,
        sum(recognized_revenue) as recognized_revenue,
        sum(sold_passenger_nights) as sold_passenger_nights
    from {{ ref('fct_revenue_recognition') }}
    group by 1, 2, 3
),
occupancy as (
    select
        month_start,
        region,
        ship_class,
        sum(sold_passenger_nights) as sold_passenger_nights,
        sum(available_passenger_nights) as available_passenger_nights,
        sum(sold_passenger_nights) / nullif(sum(available_passenger_nights), 0) as occupancy_rate
    from {{ ref('fct_occupancy_daily') }}
    group by 1, 2, 3
),
bookings as (
    select
        departure_month as month_start,
        region,
        ship_class,
        sum(bookings) as bookings,
        sum(cancellations) as cancellations,
        sum(net_booking_revenue) as net_booking_revenue
    from {{ ref('fct_booking_daily') }}
    group by 1, 2, 3
)
select
    a.target_month as month_start,
    a.region,
    a.ship_class,
    a.revenue_target,
    a.occupancy_target,
    a.booking_target,
    coalesce(r.recognized_revenue, 0) as recognized_revenue,
    coalesce(b.net_booking_revenue, 0) as net_booking_revenue,
    coalesce(o.occupancy_rate, 0) as occupancy_rate,
    coalesce(b.bookings, 0) as bookings,
    coalesce(b.cancellations, 0) as cancellations,
    coalesce(r.recognized_revenue, 0) / nullif(a.revenue_target, 0) as revenue_aop_attainment,
    coalesce(o.occupancy_rate, 0) / nullif(a.occupancy_target, 0) as occupancy_aop_attainment,
    coalesce(b.bookings, 0) / nullif(a.booking_target, 0) as booking_aop_attainment,
    coalesce(r.recognized_revenue, 0) / nullif(r.sold_passenger_nights, 0) as revenue_per_passenger_night
from {{ ref('stg_aop_targets') }} a
left join revenue r on a.target_month = r.month_start and a.region = r.region and a.ship_class = r.ship_class
left join occupancy o on a.target_month = o.month_start and a.region = o.region and a.ship_class = o.ship_class
left join bookings b on a.target_month = b.month_start and a.region = b.region and a.ship_class = b.ship_class
