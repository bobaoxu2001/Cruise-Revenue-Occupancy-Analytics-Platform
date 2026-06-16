from __future__ import annotations

from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "dbt_cruise_analytics" / "cruise_analytics.duckdb"
PROCESSED = ROOT / "data" / "processed"
TABLEAU = ROOT / "dashboards" / "tableau" / "exported_extracts"
POWERBI = ROOT / "dashboards" / "powerbi" / "exported_extracts"

MARTS = [
    "mart_executive_scorecard",
    "mart_revenue_management",
    "mart_finance_revenue",
    "mart_marketing_performance",
    "fct_occupancy_daily",
    "fct_revenue_recognition",
    "fct_booking_daily",
    "fct_campaign_performance",
]


def export_table(con: duckdb.DuckDBPyConnection, table: str, target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{table}.csv"
    con.execute(f"COPY (SELECT * FROM {table}) TO '{target.as_posix()}' (HEADER, DELIMITER ',')")


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Missing {DB_PATH}. Run dbt build first.")
    con = duckdb.connect(str(DB_PATH))
    available = {row[0] for row in con.execute("show tables").fetchall()}
    missing = [table for table in MARTS if table not in available]
    if missing:
        raise RuntimeError(f"Missing dbt mart tables: {missing}")
    for table in MARTS:
        export_table(con, table, PROCESSED)
        export_table(con, table, TABLEAU)
        export_table(con, table, POWERBI)
    print(f"Exported {len(MARTS)} governed BI extracts to data/processed, Tableau, and Power BI folders.")


if __name__ == "__main__":
    main()
