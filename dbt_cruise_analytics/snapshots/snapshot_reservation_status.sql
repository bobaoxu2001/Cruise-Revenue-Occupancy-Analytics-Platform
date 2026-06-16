{% snapshot snapshot_reservation_status %}

{{
    config(
      target_schema='snapshots',
      unique_key='reservation_id',
      strategy='timestamp',
      updated_at='updated_at'
    )
}}

select
    reservation_id,
    booking_status,
    cancellation_date,
    updated_at
from {{ ref('stg_reservations') }}

{% endsnapshot %}
