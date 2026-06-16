# Data Dictionary

## Raw and Seeded Entities

| Entity | Grain | Purpose |
| --- | --- | --- |
| `guests` | one row per guest | Loyalty, geography, acquisition channel, and age band. |
| `ships` | one row per ship | Fleet class, cabin count, and passenger capacity. |
| `cabins` | one row per cabin | Cabin category, deck, capacity, and list price multiplier. |
| `itineraries` | one row per itinerary | Region, itinerary name, ports, duration, and price multiplier. |
| `sailings` | one row per ship-itinerary departure | Departure, return date, and sailing status. |
| `reservations` | one row per cabin reservation | Booking lifecycle, passengers, gross/net amount, status, and campaign attribution. |
| `payments` | one row per payment event | Deposits, final payments, refunds, and cancellation penalties. |
| `marketing_campaigns` | one row per campaign | Campaign channel, spend, run dates, and target region. |
| `aop_targets` | one row per month-region-ship class | Revenue, occupancy, and booking plan targets. |
| `onboard_spend` | one row per onboard spend event | Optional completed-sailing service spend. |

## Intermediate Models

| Model | Grain | Key Logic |
| --- | --- | --- |
| `int_reservation_lifecycle` | reservation | Joins reservations to sailing, itinerary, capacity, status, lead time, and sold passenger nights. |
| `int_payment_events` | payment event | Adds region, ship class, departure, and recognition context to cash events. |
| `int_revenue_events` | completed reservation | Recognizes net booking revenue on sailing return date. |
| `int_sailing_capacity` | sailing | Computes available passenger nights. |
| `int_booking_lead_time` | reservation | Buckets booking lead time for pace reporting. |
| `int_campaign_attribution` | reservation | Joins campaign metadata and spend to attributed bookings. |
| `int_date_spine` | day | Date spine used by occupancy and semantic time spine. |

## Governed Marts

| Mart | Grain | Reviewer Notes |
| --- | --- | --- |
| `fct_booking_daily` | booking date, departure date, region, ship class, channel, lead-time bucket | Incremental dbt fact with gross and net booking revenue. |
| `fct_occupancy_daily` | sailing day | Uses passenger-night capacity denominator. |
| `fct_revenue_recognition` | recognition date and sailing | Separates payment timing from revenue recognition. |
| `fct_campaign_performance` | campaign | Attributed revenue, spend, ROAS, and cancellation rate. |
| `mart_executive_scorecard` | month, region, ship class | AOP attainment for revenue, occupancy, and bookings. |
| `mart_revenue_management` | sailing | Occupancy gap, booked revenue, and underperforming voyages. |
| `mart_finance_revenue` | sailing | Cash, recognized revenue, deferred revenue, refunds, and penalties. |
| `mart_finance_revenue_waterfall_monthly` | accounting month, region, ship class | Deferred revenue roll-forward and recognition rate. |
| `mart_marketing_performance` | campaign | Campaign contribution, ROAS, and cancellation exposure. |

## BI Extracts

`scripts/export_bi_extracts.py` exports governed marts into:

- `data/processed`
- `dashboards/tableau/exported_extracts`
- `dashboards/powerbi/exported_extracts`

Raw data, dbt seeds, local DuckDB databases, and profiles remain generated artifacts and are intentionally ignored by git.
