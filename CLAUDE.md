# Project Instructions

- Preserve the governed business metric definitions in `docs/metric_definitions.md` and `dbt_cruise_analytics/models/semantic/metrics.yml`.
- Run synthetic data validation before declaring model work complete.
- Do not fake Tableau, Power BI, or Snowflake screenshots. Use placeholders unless real assets are produced.
- Prefer dbt models and tests over one-off SQL patches.
- Update docs when models, grains, or metrics change.
- Keep Snowflake compatibility in mind, even though local execution uses DuckDB for reproducibility.
- Never commit secrets, warehouse credentials, or personal access tokens.
- Treat revenue recognition carefully: payment date is cash timing; recognized revenue belongs to completed sailings.
