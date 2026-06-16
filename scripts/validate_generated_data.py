from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"


def load(name: str) -> pd.DataFrame:
    path = RAW / f"{name}.csv"
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Run scripts/generate_synthetic_cruise_data.py first.")
    return pd.read_csv(path)


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    reservations = load("reservations")
    payments = load("payments")
    sailings = load("sailings")
    aop = load("aop_targets")
    ships = load("ships")
    itineraries = load("itineraries")

    assert_true(reservations["reservation_id"].is_unique, "reservation_id must be unique")
    assert_true(payments["payment_id"].is_unique, "payment_id must be unique")
    assert_true((reservations["passenger_count"] > 0).all(), "passenger_count must be positive")
    cancelled = reservations["booking_status"].eq("cancelled")
    assert_true(reservations.loc[cancelled, "cancellation_date"].notna().all(), "cancelled bookings need cancellation_date")

    sailing_dates = sailings.assign(
        departure_date=pd.to_datetime(sailings["departure_date"]),
        return_date=pd.to_datetime(sailings["return_date"]),
    )
    assert_true((sailing_dates["return_date"] > sailing_dates["departure_date"]).all(), "return_date must be after departure_date")

    final_payments = payments[payments["payment_type"].eq("final_payment")].merge(
        reservations[["reservation_id", "sailing_id"]], on="reservation_id"
    ).merge(sailings[["sailing_id", "departure_date"]], on="sailing_id")
    final_payments["payment_date"] = pd.to_datetime(final_payments["payment_date"])
    final_payments["departure_date"] = pd.to_datetime(final_payments["departure_date"])
    assert_true((final_payments["payment_date"] < final_payments["departure_date"]).all(), "final payments must be before departure")

    enriched_sailings = sailings.merge(ships[["ship_id", "ship_class"]], on="ship_id").merge(
        itineraries[["itinerary_id", "region"]], on="itinerary_id"
    )
    enriched_sailings["target_month"] = pd.to_datetime(enriched_sailings["departure_date"]).dt.to_period("M").dt.to_timestamp()
    aop_key = set(zip(pd.to_datetime(aop["target_month"]).dt.to_period("M").astype(str), aop["region"], aop["ship_class"]))
    sailing_key = set(zip(enriched_sailings["target_month"].dt.to_period("M").astype(str), enriched_sailings["region"], enriched_sailings["ship_class"]))
    assert_true(sailing_key.issubset(aop_key), "AOP target coverage missing for one or more month-region-ship_class combinations")

    print("Synthetic data validation passed.")
    print(f"Rows: reservations={len(reservations):,}, payments={len(payments):,}, sailings={len(sailings):,}, aop_targets={len(aop):,}")


if __name__ == "__main__":
    main()
