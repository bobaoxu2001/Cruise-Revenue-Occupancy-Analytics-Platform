# AI Tooling Case Study

This project uses AI-assisted engineering in the same way an analytics team might use Claude Code, Cursor, or similar tools: to accelerate drafts, spot issues, and reduce repetitive work. It does not claim autonomous production deployment.

## What AI Helped With

- Generated the initial dbt project skeleton across staging, intermediate, mart, semantic, snapshot, exposure, and test folders.
- Suggested business-rule tests from metric requirements, including occupancy caps, nonnegative recognized revenue, final-payment timing, AOP target coverage, and cancellation date completeness.
- Helped identify grain mismatches between daily occupancy facts, sailing-level finance marts, and month-region-ship class executive scorecards.
- Helped refactor repeated joins into intermediate models such as `int_reservation_lifecycle`, `int_payment_events`, and `int_sailing_capacity`.
- Drafted first-pass documentation for metric definitions, data dictionary, dashboard rebuild instructions, and the PR checklist.
- Helped debug semantic-layer validation issues in CI by adjusting metric references, time spine requirements, and entity naming.

## What Required Human Review

- Finance logic: revenue recognition belongs to completed sailings, while cash collection belongs to payment dates.
- Occupancy denominator: passenger nights were chosen over cabins to match cruise capacity planning.
- Metric governance: placeholder metrics were removed when they did not reflect actual source fields.
- BI grain decisions: sailing-level, daily, campaign-level, and monthly scorecard facts were kept separate to avoid double counting.
- Claims discipline: no fake Tableau, Power BI, or Snowflake deployment artifacts are presented.

## Practical Outcome

AI sped up scaffolding and iteration, but the final work still depends on analytics engineering judgment: clear grains, stable business definitions, repeatable tests, and honest documentation of what is implemented locally versus Snowflake-ready.
