# Power BI Finance Revenue Recognition Scorecard Blueprint

Data sources:
- `mart_finance_revenue.csv`
- `fct_revenue_recognition.csv`
- `mart_executive_scorecard.csv`

Pages:
- Deferred revenue trend.
- Recognized revenue waterfall.
- Refund exposure and cancellation penalties.
- Monthly AOP attainment.
- Revenue recognition by region and ship class.

DAX-style measures:
- Deferred Revenue = SUM(mart_finance_revenue[deferred_revenue])
- Recognized Revenue = SUM(mart_finance_revenue[recognized_revenue])
- Refund Exposure = SUM(mart_finance_revenue[refund_exposure])
- AOP Attainment = DIVIDE(SUM(mart_executive_scorecard[recognized_revenue]), SUM(mart_executive_scorecard[revenue_target]))

Manual rebuild:
1. Import the exported CSVs.
2. Mark the month field as date.
3. Build relationships only at compatible grains.
4. Use the measures above rather than redefining finance logic in visuals.
