"""Run a lightweight local DuckDB build of the dbt SQL models.

This is a smoke-test helper for development environments where the dbt CLI is
not installed. It does not replace dbt build, docs, snapshots, or lineage, but
it validates that the model SQL and singular business-rule tests execute
against the generated CSV seeds.
"""

from __future__ import annotations

import re
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "dbt_cruise_analytics" / "cruise_analytics.duckdb"
SEED_DIR = ROOT / "dbt_cruise_analytics" / "seeds"
MODEL_DIR = ROOT / "dbt_cruise_analytics" / "models"
TEST_DIR = ROOT / "dbt_cruise_analytics" / "tests"

SEEDS = [
    "guests",
    "ships",
    "cabins",
    "itineraries",
    "sailings",
    "reservations",
    "payments",
    "marketing_campaigns",
    "aop_targets",
    "onboard_spend",
]

MODEL_ORDER = [
    *(f"staging/stg_{name}" for name in SEEDS),
    "intermediate/int_date_spine",
    "intermediate/int_sailing_capacity",
    "intermediate/int_reservation_lifecycle",
    "intermediate/int_payment_events",
    "intermediate/int_revenue_events",
    "intermediate/int_booking_lead_time",
    "intermediate/int_campaign_attribution",
    "marts/dim_guest",
    "marts/dim_ship",
    "marts/dim_itinerary",
    "marts/dim_sailing",
    "marts/fct_booking_daily",
    "marts/fct_revenue_recognition",
    "marts/fct_occupancy_daily",
    "marts/fct_campaign_performance",
    "marts/mart_executive_scorecard",
    "marts/mart_revenue_management",
    "marts/mart_finance_revenue",
    "marts/mart_finance_revenue_waterfall_monthly",
    "marts/mart_marketing_performance",
    "semantic/metricflow_time_spine",
]


def compile_refs(sql: str) -> str:
    sql = re.sub(r"\{\{\s*config\([\s\S]*?\)\s*\}\}", "", sql)
    sql = re.sub(r"\{% if is_incremental\(\) %\}[\s\S]*?\{% endif %\}", "", sql)
    return re.sub(r"\{\{\s*ref\('([^']+)'\)\s*\}\}", r"\1", sql)


def main() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
    con = duckdb.connect(str(DB_PATH))

    for seed in SEEDS:
        csv_path = SEED_DIR / f"{seed}.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing {csv_path}. Run synthetic data generation first.")
        con.execute(
            f"create or replace table {seed} as "
            f"select * from read_csv_auto('{csv_path.as_posix()}', header=true)"
        )

    for model in MODEL_ORDER:
        sql_path = MODEL_DIR / f"{model}.sql"
        sql = compile_refs(sql_path.read_text(encoding="utf-8")).strip().rstrip(";")
        relation = model.split("/")[-1]
        materialization = "view" if model.startswith("staging/") else "table"
        con.execute(f"create or replace {materialization} {relation} as {sql}")

    failures = []
    for test_path in sorted(TEST_DIR.glob("*.sql")):
        sql = compile_refs(test_path.read_text(encoding="utf-8")).strip().rstrip(";")
        count = con.execute(f"select count(*) from ({sql}) as test_failures").fetchone()[0]
        if count:
            failures.append((test_path.name, count))

    if failures:
        detail = ", ".join(f"{name}={count}" for name, count in failures)
        raise AssertionError(f"DuckDB smoke tests failed: {detail}")

    mart_count = con.execute("select count(*) from mart_executive_scorecard").fetchone()[0]
    print(f"Local DuckDB smoke build passed. mart_executive_scorecard rows={mart_count:,}.")


if __name__ == "__main__":
    main()
