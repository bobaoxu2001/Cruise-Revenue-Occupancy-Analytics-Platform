# Power BI Data Source Mapping

Connect Power BI Desktop to `dashboards/powerbi/exported_extracts`.

Recommended model:
- Fact: `mart_finance_revenue`
- Fact: `mart_finance_revenue_waterfall_monthly`
- Fact: `fct_revenue_recognition`
- Scorecard: `mart_executive_scorecard`

Grain guidance:
- `mart_finance_revenue` is one row per sailing.
- `mart_finance_revenue_waterfall_monthly` is one row per accounting month, region, and ship class.
- `fct_revenue_recognition` is recognition date and sailing grain.
- `mart_executive_scorecard` is month, region, and ship class grain.

Avoid joining two fact tables directly at incompatible grains. Use month, region, and ship class only for aggregate visuals, and use sailing-level tables for drill-through pages.
