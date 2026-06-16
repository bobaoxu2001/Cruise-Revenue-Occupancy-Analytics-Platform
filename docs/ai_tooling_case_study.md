# AI Tooling Case Study

This project documents practical AI-assisted analytics engineering, not magic automation.

Claude Code / Cursor-style tooling helped accelerate:
- Initial dbt model skeletons for staging, intermediate, and mart layers.
- Translation of business rules into dbt tests, including occupancy caps and revenue recognition checks.
- SQL debugging by narrowing model failures to grain mismatches, date casts, and null campaign attribution.
- Documentation drafts for data dictionary, metric definitions, dashboard rebuild instructions, and CI checklists.
- Refactoring repeated SQL patterns into reusable intermediate models.

Human review remained necessary for metric governance, finance logic, dashboard grain decisions, and validation. The project intentionally avoids claiming live Snowflake Cortex, Tableau, or Power BI automation without credentials and produced artifacts.
