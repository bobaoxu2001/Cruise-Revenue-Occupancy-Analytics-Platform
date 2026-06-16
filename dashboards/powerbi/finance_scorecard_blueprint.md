# Power BI Finance Revenue Recognition Scorecard Blueprint

Data sources:
- `mart_finance_revenue.csv`
- `mart_finance_revenue_waterfall_monthly.csv`
- `fct_revenue_recognition.csv`
- `mart_executive_scorecard.csv`

Pages:
- Deferred revenue trend.
- Recognized revenue waterfall.
- Monthly deferred revenue roll-forward by region and ship class.
- Refund exposure and cancellation penalties.
- Monthly AOP attainment.
- Revenue recognition by region and ship class.

DAX-style measures:
- Deferred Revenue = SUM(mart_finance_revenue[deferred_revenue])
- Beginning Deferred Revenue = SUM(mart_finance_revenue_waterfall_monthly[beginning_deferred_revenue])
- Ending Deferred Revenue = SUM(mart_finance_revenue_waterfall_monthly[ending_deferred_revenue])
- Recognized Revenue = SUM(mart_finance_revenue[recognized_revenue])
- Refund Exposure = SUM(mart_finance_revenue[refund_exposure])
- Net Cash Activity = SUM(mart_finance_revenue_waterfall_monthly[net_cash_activity])
- AOP Attainment = DIVIDE(SUM(mart_executive_scorecard[recognized_revenue]), SUM(mart_executive_scorecard[revenue_target]))

Manual rebuild:
1. Import the exported CSVs.
2. Mark the month field as date.
3. Use `mart_finance_revenue_waterfall_monthly` for monthly roll-forward visuals.
4. Keep `mart_finance_revenue` at sailing grain for drill-through and refund exposure.
5. Build relationships only at compatible grains.
6. Use the measures above rather than redefining finance logic in visuals.
