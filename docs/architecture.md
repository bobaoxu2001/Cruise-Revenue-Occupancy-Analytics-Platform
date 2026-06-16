# Architecture

```mermaid
flowchart LR
    A[Python synthetic data generator] --> B[CSV raw data]
    B --> C[dbt seeds in DuckDB]
    C --> D[Staging models]
    D --> E[Intermediate business logic]
    E --> F[Governed marts]
    F --> G[Tableau extracts]
    F --> H[Power BI extracts]
    F --> I[Streamlit governed AI analyst]
    F --> J[dbt docs and exposures]
```

The local platform uses DuckDB for reproducibility. The model design mirrors a Snowflake deployment: raw ingestion, cleaned staging, reusable intermediate models, governed marts, semantic metrics, and downstream BI extracts.
