# Tableau Data Source Mapping

Connect Tableau Public/Desktop to the CSV files in `dashboards/tableau/exported_extracts`.

Primary tables:
- `mart_executive_scorecard`: executive KPIs and AOP attainment.
- `mart_revenue_management`: sailing-level occupancy gaps and booked revenue.
- `mart_marketing_performance`: campaign ROAS and contribution.

Recommended relationships:
- Relate on `region`, `ship_class`, and month fields where applicable.
- Keep `mart_revenue_management` at sailing grain to avoid double counting.
