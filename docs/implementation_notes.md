# Implementation Notes

- DuckDB is used locally to make the project reproducible without cloud credentials.
- dbt seeds are generated from the same deterministic source files as `data/raw`.
- The semantic YAML is written in a MetricFlow/dbt-semantic-layer style but is documented as illustrative because this local build does not require MetricFlow.
- Tableau and Power BI dashboard files are blueprints plus exported CSV extracts; no fake screenshots are committed.
- Snowflake examples are standalone patterns designed to demonstrate warehouse-ready SQL.
