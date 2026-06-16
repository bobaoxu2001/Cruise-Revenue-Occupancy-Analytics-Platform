# Metric Definitions

These metrics are governed in dbt models and mirrored in `dbt_cruise_analytics/models/semantic/metrics.yml`. Payment timing and revenue recognition timing are intentionally separate.

| Metric | Business Definition | Formula | Source Model | Grain | Caveats |
| --- | --- | --- | --- | --- | --- |
| gross_booking_revenue | Reservation demand before discounts. | `sum(gross_booking_amount)` | `fct_booking_daily` | booking date, departure date, region, ship class, booking channel, lead-time bucket | Does not remove cancellations unless filtered by status upstream. |
| net_booking_revenue | Reservation demand after discounts. | `sum(net_booking_amount)` | `fct_booking_daily`, `mart_executive_scorecard` | daily booking grain or monthly scorecard grain | Booking revenue is not the same as recognized revenue. |
| recognized_revenue | Revenue recognized after a sailing is completed. | `sum(net_booking_amount)` for completed reservations, recognized on sailing return date | `fct_revenue_recognition`, `mart_finance_revenue` | recognition date and sailing | Excludes future confirmed sailings and cancelled bookings. |
| deferred_revenue | Cash collected for revenue not yet recognized. | `cash_collected - recognized_revenue`, floored at zero in sailing mart | `mart_finance_revenue` | sailing | Sailing-level mart is a point-in-time simplification for portfolio review. |
| beginning_deferred_revenue | Deferred revenue balance before monthly activity. | prior month ending deferred by region and ship class | `mart_finance_revenue_waterfall_monthly` | accounting month, region, ship class | Computed from synthetic payment and recognition events. |
| ending_deferred_revenue | Deferred revenue after monthly cash, refunds, penalties, and recognition. | `beginning_deferred_revenue + cash_collected + cancellation_penalties + refunds - recognized_revenue` | `mart_finance_revenue_waterfall_monthly` | accounting month, region, ship class | Refunds are stored as negative payment amounts. |
| occupancy_rate | Share of available passenger-night capacity sold. | `sold_passenger_nights / available_passenger_nights` | `fct_occupancy_daily`, `mart_executive_scorecard` | daily sailing or monthly scorecard | Uses passenger nights, not cabins, as denominator. |
| booking_pace | Bookings by lead time before departure. | `sum(bookings)` by `lead_time_bucket` | `fct_booking_daily` | booking date, departure date, region, ship class, channel, lead-time bucket | Lead-time buckets are derived in `int_booking_lead_time`. |
| cancellation_rate | Share of bookings cancelled. | `cancelled_bookings / bookings` | `fct_booking_daily`, `mart_marketing_performance` | channel, campaign, or scorecard grain | Rates should be interpreted at compatible grains only. |
| AOP attainment | Actual performance versus Annual Operating Plan. | `actual / target` for revenue, occupancy, or bookings | `mart_executive_scorecard` | month, region, ship class | Requires AOP targets for every month-region-ship class used in reporting. |
| revenue_per_passenger_night | Revenue yield per sold passenger night. | `recognized_revenue / sold_passenger_nights` | `fct_revenue_recognition`, `mart_executive_scorecard` | recognition month, region, ship class, or sailing | Only meaningful for completed sailings. |
| campaign_roas | Attributed booking revenue per dollar of media spend. | `attributed_net_revenue / campaign_spend` | `mart_marketing_performance` | campaign | Null when campaign spend is zero. Organic/unattributed bookings are grouped separately. |
| refund_exposure | Cash refunded to guests. | `abs(sum(refund payment_amount))` | `mart_finance_revenue` | sailing | Refund payment rows are negative in raw payments. |
| cancellation_penalties | Penalties retained on cancelled bookings. | `sum(cancellation_penalty payment_amount)` | `mart_finance_revenue`, `mart_finance_revenue_waterfall_monthly` | sailing or accounting month | Modeled as positive cash activity. |
| net_cash_activity | Monthly cash movement before revenue recognition. | `cash_collected + cancellation_penalties + refunds` | `mart_finance_revenue_waterfall_monthly` | accounting month, region, ship class | Refunds reduce net cash because they are negative amounts. |
| revenue_recognition_rate | Portion of available deferred-plus-new cash recognized in the month. | `recognized_revenue / (beginning_deferred_revenue + net_cash_activity)` | `mart_finance_revenue_waterfall_monthly` | accounting month, region, ship class | Useful as a finance diagnostic, not a GAAP disclosure. |

## Sign Conventions

- Deposit and final payment rows are positive cash inflows.
- Refund rows are negative cash outflows.
- Cancellation penalties are positive retained cash.
- Recognized revenue is tied to sailing completion, not payment date.
