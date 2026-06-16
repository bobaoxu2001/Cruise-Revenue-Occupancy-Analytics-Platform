select * from {{ ref('stg_sailings') }} where return_date <= departure_date
