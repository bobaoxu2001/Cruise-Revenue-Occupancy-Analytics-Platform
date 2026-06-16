# Power BI Data Source Mapping

Connect Power BI Desktop to `dashboards/powerbi/exported_extracts`.

Recommended model:
- Fact: `mart_finance_revenue`
- Fact: `fct_revenue_recognition`
- Scorecard: `mart_executive_scorecard`

Avoid joining two fact tables directly at incompatible grains. Use month, region, and ship class only for aggregate visuals.
