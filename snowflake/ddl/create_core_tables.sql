create schema if not exists raw_cruise;
create schema if not exists analytics;

create or replace table raw_cruise.reservations (
    reservation_id varchar,
    guest_id varchar,
    sailing_id varchar,
    cabin_id varchar,
    booking_date date,
    booking_status varchar,
    cancellation_date date,
    booking_channel varchar,
    campaign_id varchar,
    passenger_count number,
    gross_booking_amount number(18, 2),
    discount_amount number(18, 2),
    net_booking_amount number(18, 2),
    currency varchar,
    updated_at timestamp
);
