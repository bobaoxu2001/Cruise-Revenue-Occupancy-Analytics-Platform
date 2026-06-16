# Hiring Manager Walkthrough

## Five-Minute Review Path

1. Read the first two sections of `README.md` for scope and the implemented-vs-Snowflake-ready table.
2. Inspect `dbt_cruise_analytics/models/marts/fct_booking_daily.sql` for a real incremental dbt model and stable grain.
3. Inspect `dbt_cruise_analytics/models/marts/mart_finance_revenue_waterfall_monthly.sql` for deferred revenue roll-forward logic.
4. Review `dbt_cruise_analytics/models/semantic/metrics.yml` and `docs/metric_definitions.md` for governed KPI definitions.
5. Open `dbt_cruise_analytics/models/marts/schema.yml` and `dbt_cruise_analytics/tests` for final-model quality checks.
6. Review `snowflake/sql_examples` for Snowflake-specific SQL depth.
7. Check `dashboards/tableau` and `dashboards/powerbi` for BI rebuild instructions and exported data assets.
8. Review `.github/workflows/ci.yml` for reproducible CI.

## Snowflake SQL Strength

Inspect:

- `snowflake/sql_examples/recursive_cte_date_spine.sql`
- `snowflake/sql_examples/window_booking_pace.sql`
- `snowflake/sql_examples/incremental_merge_booking_daily.sql`
- `snowflake/sql_examples/revenue_recognition_waterfall.sql`
- `snowflake/sql_examples/row_level_security_policy_example.sql`

These examples show recursive CTEs, window functions, MERGE-style incremental loading, finance waterfall logic, and regional row-level security.

## dbt Production Discipline

Inspect:

- `models/staging` for typed source cleanup.
- `models/intermediate` for reusable lifecycle, payment, capacity, and revenue logic.
- `models/marts` for governed facts and marts.
- `models/marts/fct_booking_daily.sql` for incremental materialization.
- `snapshots/snapshot_reservation_status.sql` for reservation status tracking.
- `models/exposures.yml` for BI lineage.
- `models/marts/schema.yml` and `tests/` for data quality.

The project has CI that runs data generation, validation, dbt deps/debug/build/docs, export checks, and Streamlit syntax checks.

## Finance and Revenue Recognition Depth

Inspect:

- `int_revenue_events.sql`: recognizes revenue on completed sailings.
- `mart_finance_revenue.sql`: sailing-level cash, refunds, penalties, recognized revenue, and deferred revenue.
- `mart_finance_revenue_waterfall_monthly.sql`: monthly beginning deferred, cash activity, refunds, penalties, recognition, and ending deferred.
- `docs/metric_definitions.md`: sign conventions and formulas.

The key finance distinction is that payment date is cash timing; sailing completion drives revenue recognition.

## BI Readiness

Inspect:

- `dashboards/tableau/executive_scorecard_blueprint.md`
- `dashboards/tableau/data_source_mapping.md`
- `dashboards/powerbi/finance_scorecard_blueprint.md`
- `dashboards/powerbi/data_source_mapping.md`
- `dashboards/*/exported_extracts`

The repository includes exported CSV extracts for manual Tableau and Power BI builds. It does not claim fabricated dashboard screenshots.

## AI Tooling

Inspect:

- `docs/ai_tooling_case_study.md`
- `CLAUDE.md`
- `.github/pull_request_template.md`

The AI tooling story is intentionally practical: AI accelerated skeleton creation, test suggestions, SQL debugging, docs, and checklist drafting, while metric logic and finance assumptions remained human-reviewed.

## Implemented vs Snowflake-Ready

Implemented locally:

- Synthetic data generator.
- DuckDB/dbt-duckdb project.
- Staging, intermediate, mart, snapshot, semantic, and exposure files.
- Incremental dbt booking fact.
- Monthly finance revenue waterfall.
- BI extracts.
- Streamlit governed analyst demo.
- GitHub Actions CI.

Snowflake-ready but not deployed:

- Snowflake DDL and SQL examples.
- MERGE pattern.
- Row access policy example.
- Deployment guide.
- Warehouse performance notes.

No Snowflake deployment is claimed because credentials are not included.

## Manual Next Steps for Tableau and Power BI Screenshots

1. Run the project locally or use the committed exported extracts.
2. Open Tableau Desktop/Public and connect to `dashboards/tableau/exported_extracts`.
3. Rebuild the executive scorecard from the Tableau blueprint.
4. Open Power BI Desktop and connect to `dashboards/powerbi/exported_extracts`.
5. Rebuild the finance scorecard and monthly waterfall from the Power BI blueprint.
6. Save real screenshots to `docs/screenshots` only after the dashboards are actually built.
