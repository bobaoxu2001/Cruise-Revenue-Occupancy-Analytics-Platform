## Summary

- 

## Validation

- [ ] `python scripts/generate_synthetic_cruise_data.py`
- [ ] `python scripts/validate_generated_data.py`
- [ ] `cd dbt_cruise_analytics && cp profiles.example.yml profiles.yml && dbt deps && dbt build --profiles-dir .`
- [ ] `python scripts/local_duckdb_smoke_build.py` when dbt CLI is unavailable locally
- [ ] `python scripts/export_bi_extracts.py`
- [ ] Streamlit import check

## Analytics Governance Checklist

- [ ] Metric definitions were preserved or intentionally updated.
- [ ] dbt tests cover new business rules.
- [ ] Tableau/Power BI mappings still reference governed marts.
- [ ] No secrets, credentials, or generated warehouse artifacts are committed.
