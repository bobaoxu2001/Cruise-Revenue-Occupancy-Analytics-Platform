-- Snowflake incremental MERGE pattern for a daily booking aggregate.
merge into analytics.fct_booking_daily as target
using (
    select
        booking_date,
        region,
        ship_class,
        booking_channel,
        count(*) as bookings,
        sum(net_booking_amount) as net_booking_revenue
    from analytics.int_reservation_lifecycle
    where booking_date >= dateadd(day, -7, current_date)
    group by 1, 2, 3, 4
) as source
on target.booking_date = source.booking_date
and target.region = source.region
and target.ship_class = source.ship_class
and target.booking_channel = source.booking_channel
when matched then update set
    bookings = source.bookings,
    net_booking_revenue = source.net_booking_revenue,
    updated_at = current_timestamp
when not matched then insert (
    booking_date, region, ship_class, booking_channel, bookings, net_booking_revenue, updated_at
) values (
    source.booking_date, source.region, source.ship_class, source.booking_channel,
    source.bookings, source.net_booking_revenue, current_timestamp
);
