# Tableau Executive Scorecard Blueprint

Data sources:
- `mart_executive_scorecard.csv`
- `mart_revenue_management.csv`
- `mart_marketing_performance.csv`

Views:
- Revenue vs AOP by month, region, and ship class.
- Occupancy by region, ship, and itinerary.
- Booking pace by departure month and lead-time bucket.
- Cancellation rate by booking channel.
- Revenue per passenger night.
- Campaign contribution and ROAS.
- Top underperforming sailings by occupancy gap.

Filters:
- Month
- Region
- Ship class
- Itinerary
- Booking channel

Calculated fields:
- Revenue AOP attainment = recognized revenue / revenue target.
- Occupancy gap = 1 - occupancy rate.
- Campaign contribution = attributed net revenue - campaign spend.

Row-level security assumption:
- Production Tableau would pass user region entitlements from the identity provider or a Snowflake row access policy.

Generated proof asset:
- `docs/screenshots/tableau_executive_scorecard.png` is generated from the governed extracts by `scripts/generate_dashboard_screenshots.py`.

Tableau Public publish path:
1. Sign in to Tableau Public.
2. Create a new workbook from the CSV extracts in `dashboards/tableau/exported_extracts`.
3. Rebuild the views listed above.
4. Publish the workbook publicly.
5. Replace the placeholder Tableau exposure URL in `dbt_cruise_analytics/models/exposures.yml` with the real Tableau Public URL.
