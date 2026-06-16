# Five-Minute Hiring Manager Walkthrough

1. Start with `README.md` for the architecture and role alignment.
2. Inspect `scripts/generate_synthetic_cruise_data.py` to see realistic cruise data generation and edge cases.
3. Review `dbt_cruise_analytics/models/staging`, `intermediate`, and `marts` for layered dbt modeling.
4. Open `dbt_cruise_analytics/tests` for business-rule tests.
5. Check `dbt_cruise_analytics/models/semantic/metrics.yml` and `docs/metric_definitions.md` for governed KPI definitions.
6. Inspect `snowflake/sql_examples` for recursive CTE, window, MERGE, revenue waterfall, and security examples.
7. Review `dashboards/tableau` and `dashboards/powerbi` for BI rebuild plans and data source mappings.
8. Open `.github/workflows/ci.yml` for CI discipline.
9. Try `streamlit_app/app.py` for controlled, governed business Q&A.
