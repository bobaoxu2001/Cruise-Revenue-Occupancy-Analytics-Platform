# Snowflake Deployment Guide

Local execution uses DuckDB so the project can be reviewed without warehouse credentials. To deploy to Snowflake:

1. Create `raw_cruise`, `analytics`, and `snapshots` schemas.
2. Load generated CSVs from `data/raw` to an internal stage.
3. Configure a `dbt-snowflake` profile with account, warehouse, database, role, and schema.
4. Replace the DuckDB profile with the Snowflake target.
5. Run `dbt deps`, `dbt seed`, `dbt build`, and `dbt docs generate`.
6. Apply row access policies after validating regional access rules.

No real Snowflake deployment is claimed by this repository.
