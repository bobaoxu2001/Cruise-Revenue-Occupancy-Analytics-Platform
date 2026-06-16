"""Generate deterministic synthetic cruise analytics data.

The data is intentionally realistic enough to exercise analytics engineering
logic: revenue recognition by sailing completion, deferred revenue, refunds,
campaign attribution, booking pace, occupancy denominators, and AOP targets.
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
SEED_DIR = ROOT / "dbt_cruise_analytics" / "seeds"
SAMPLE_DIR = ROOT / "data" / "samples"
RNG = np.random.default_rng(20250616)
AS_OF_DATE = date(2026, 6, 16)


def save(df: pd.DataFrame, name: str) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    SEED_DIR.mkdir(parents=True, exist_ok=True)
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(RAW_DIR / f"{name}.csv", index=False)
    df.to_csv(SEED_DIR / f"{name}.csv", index=False)
    df.head(250).to_csv(SAMPLE_DIR / f"{name}_sample.csv", index=False)


def choice(values, p=None):
    return RNG.choice(values, p=p)


def make_guests(n: int = 4200) -> pd.DataFrame:
    countries = ["US", "CA", "GB", "AU", "DE", "FR", "JP", "KR", "BR", "MX"]
    states = ["CA", "FL", "NY", "TX", "WA", "IL", "GA", "MA", "BC", "ON", ""]
    tiers = ["Classic", "Silver", "Gold", "Platinum", "Diamond"]
    channels = ["Paid Search", "Email", "Travel Advisor", "Direct", "Social", "Organic"]
    rows = []
    for i in range(1, n + 1):
        first_booking = date(2023, 1, 1) + timedelta(days=int(RNG.integers(0, 1050)))
        rows.append(
            {
                "guest_id": f"G{i:06d}",
                "loyalty_tier": choice(tiers, p=[0.40, 0.24, 0.18, 0.12, 0.06]),
                "home_country": choice(countries, p=[0.54, 0.10, 0.09, 0.06, 0.05, 0.04, 0.04, 0.03, 0.03, 0.02]),
                "home_state": choice(states),
                "acquisition_channel": choice(channels, p=[0.18, 0.17, 0.24, 0.20, 0.08, 0.13]),
                "first_booking_date": first_booking.isoformat(),
                "age_band": choice(["25-34", "35-44", "45-54", "55-64", "65+"], p=[0.12, 0.19, 0.26, 0.27, 0.16]),
            }
        )
    return pd.DataFrame(rows)


def make_ships() -> pd.DataFrame:
    rows = [
        ("S001", "Celestia", "Expedition", 72, 148),
        ("S002", "Aurelia", "Ocean", 96, 202),
        ("S003", "Odyssey", "Ocean", 110, 232),
        ("S004", "Serenity", "Yacht", 58, 116),
        ("S005", "Meridian", "River", 64, 128),
        ("S006", "Elysian", "Expedition", 78, 158),
    ]
    return pd.DataFrame(rows, columns=["ship_id", "ship_name", "ship_class", "total_cabins", "passenger_capacity"])


def make_cabins(ships: pd.DataFrame) -> pd.DataFrame:
    cats = [
        ("Ocean Suite", 2, 1.00),
        ("Veranda Suite", 2, 1.18),
        ("Penthouse", 3, 1.65),
        ("Owner Suite", 4, 2.20),
    ]
    rows = []
    for ship in ships.itertuples(index=False):
        for idx in range(1, ship.total_cabins + 1):
            cat, capacity, mult = cats[min(len(cats) - 1, int(RNG.choice([0, 1, 2, 3], p=[0.45, 0.34, 0.16, 0.05])))]
            rows.append(
                {
                    "cabin_id": f"{ship.ship_id}-C{idx:03d}",
                    "ship_id": ship.ship_id,
                    "cabin_category": cat,
                    "deck": int(RNG.integers(3, 11)),
                    "capacity": capacity,
                    "list_price_multiplier": round(mult, 2),
                }
            )
    return pd.DataFrame(rows)


def make_itineraries() -> pd.DataFrame:
    specs = [
        ("CAR7", "Caribbean", "Leeward Islands Retreat", "San Juan", "San Juan", 7, 1.04),
        ("CAR10", "Caribbean", "Antilles Luxury Crossing", "Miami", "Bridgetown", 10, 1.08),
        ("MED7", "Mediterranean", "Greek Isles and Amalfi", "Athens", "Rome", 7, 1.25),
        ("MED12", "Mediterranean", "Riviera Grand Voyage", "Barcelona", "Venice", 12, 1.35),
        ("ALA9", "Alaska", "Glaciers and Fjords", "Vancouver", "Seward", 9, 1.18),
        ("NOR11", "Northern Europe", "Baltic Capitals", "Copenhagen", "Stockholm", 11, 1.15),
        ("ASI14", "Asia Pacific", "Japan and Korea Discovery", "Tokyo", "Busan", 14, 1.30),
        ("RIV8", "European Rivers", "Danube Culinary Sail", "Budapest", "Vienna", 8, 1.10),
    ]
    return pd.DataFrame(
        [
            {
                "itinerary_id": s[0],
                "region": s[1],
                "itinerary_name": s[2],
                "embark_port": s[3],
                "disembark_port": s[4],
                "duration_days": s[5],
                "base_price_multiplier": s[6],
            }
            for s in specs
        ]
    )


def make_sailings(ships: pd.DataFrame, itineraries: pd.DataFrame) -> pd.DataFrame:
    rows = []
    sailing_id = 1
    start = date(2024, 1, 6)
    end = date(2026, 12, 20)
    for ship in ships.itertuples(index=False):
        current = start + timedelta(days=int(RNG.integers(0, 10)))
        while current <= end:
            eligible = itineraries.copy()
            if ship.ship_class == "River":
                eligible = eligible[eligible["region"].isin(["European Rivers", "Northern Europe"])]
            elif ship.ship_class == "Yacht":
                eligible = eligible[eligible["region"].isin(["Caribbean", "Mediterranean"])]
            itinerary = eligible.sample(1, random_state=int(RNG.integers(0, 1_000_000))).iloc[0]
            status = "completed" if current + timedelta(days=int(itinerary.duration_days)) < AS_OF_DATE else "scheduled"
            rows.append(
                {
                    "sailing_id": f"SA{sailing_id:05d}",
                    "ship_id": ship.ship_id,
                    "itinerary_id": itinerary.itinerary_id,
                    "departure_date": current.isoformat(),
                    "return_date": (current + timedelta(days=int(itinerary.duration_days))).isoformat(),
                    "sailing_status": status,
                }
            )
            sailing_id += 1
            current += timedelta(days=int(itinerary.duration_days + RNG.integers(3, 8)))
    return pd.DataFrame(rows)


def make_campaigns(itineraries: pd.DataFrame) -> pd.DataFrame:
    rows = []
    channels = ["Paid Search", "Email", "Travel Advisor", "Social", "Display"]
    for i in range(1, 49):
        start = date(2023, 10, 1) + timedelta(days=int((i - 1) * 22))
        region = choice(sorted(itineraries["region"].unique()))
        channel = choice(channels, p=[0.32, 0.22, 0.20, 0.16, 0.10])
        rows.append(
            {
                "campaign_id": f"CMP{i:04d}",
                "channel": channel,
                "campaign_name": f"{region} {channel} Wave {i:02d}",
                "start_date": start.isoformat(),
                "end_date": (start + timedelta(days=45)).isoformat(),
                "spend": round(float(RNG.uniform(18000, 95000)), 2),
                "target_region": region,
            }
        )
    return pd.DataFrame(rows)


def make_reservations_and_payments(guests, ships, cabins, itineraries, sailings, campaigns):
    ship_lookup = ships.set_index("ship_id").to_dict("index")
    itin_lookup = itineraries.set_index("itinerary_id").to_dict("index")
    cabin_lookup = cabins.set_index("cabin_id").to_dict("index")
    cabin_by_ship = {ship_id: df["cabin_id"].tolist() for ship_id, df in cabins.groupby("ship_id")}
    campaigns_by_region = {region: df for region, df in campaigns.groupby("target_region")}
    guest_ids = guests["guest_id"].tolist()
    reservations = []
    payments = []
    onboard = []
    res_num = 1
    pay_num = 1
    spend_num = 1
    for sailing in sailings.itertuples(index=False):
        ship = ship_lookup[sailing.ship_id]
        itin = itin_lookup[sailing.itinerary_id]
        departure = date.fromisoformat(sailing.departure_date)
        return_date = date.fromisoformat(sailing.return_date)
        demand = {
            "Mediterranean": 0.86,
            "Alaska": 0.82,
            "Asia Pacific": 0.76,
            "Caribbean": 0.79,
            "European Rivers": 0.73,
            "Northern Europe": 0.69,
        }[itin["region"]]
        if "Riviera" in itin["itinerary_name"] or "Greek" in itin["itinerary_name"]:
            demand += 0.08
        if "Baltic" in itin["itinerary_name"]:
            demand -= 0.08
        cabin_ids = cabin_by_ship[sailing.ship_id].copy()
        RNG.shuffle(cabin_ids)
        cabins_to_sell = min(len(cabin_ids), max(8, int(RNG.normal(demand * len(cabin_ids), 7))))
        for cabin_id in cabin_ids[:cabins_to_sell]:
            cabin = cabin_lookup[cabin_id]
            lead_days = int(max(4, RNG.gamma(4.4, 33)))
            booking_date = departure - timedelta(days=lead_days)
            if booking_date < date(2023, 8, 1):
                booking_date = date(2023, 8, 1) + timedelta(days=int(RNG.integers(0, 20)))
            channel = choice(["Direct", "Travel Advisor", "Paid Search", "Email", "Social", "Organic"], p=[0.23, 0.29, 0.17, 0.15, 0.07, 0.09])
            region_campaigns = campaigns_by_region.get(itin["region"])
            campaign_id = ""
            if channel in ["Paid Search", "Email", "Social"] and region_campaigns is not None and RNG.random() < 0.72:
                active = region_campaigns[
                    (pd.to_datetime(region_campaigns["start_date"]).dt.date <= booking_date)
                    & (pd.to_datetime(region_campaigns["end_date"]).dt.date >= booking_date)
                ]
                if len(active) > 0:
                    campaign_id = active.sample(1, random_state=int(RNG.integers(0, 1_000_000))).iloc[0]["campaign_id"]
            passenger_count = int(min(cabin["capacity"], choice([1, 2, 3, 4], p=[0.12, 0.70, 0.13, 0.05])))
            base_daily = 580 + (95 if ship["ship_class"] == "Expedition" else 0) + (130 if ship["ship_class"] == "Yacht" else 0)
            gross = base_daily * itin["duration_days"] * passenger_count * cabin["list_price_multiplier"] * itin["base_price_multiplier"]
            if channel == "Travel Advisor":
                discount_rate = float(RNG.uniform(0.04, 0.10))
            elif lead_days < 35:
                discount_rate = float(RNG.uniform(0.08, 0.18))
            else:
                discount_rate = float(RNG.uniform(0.00, 0.07))
            discount = round(gross * discount_rate, 2)
            net = round(gross - discount, 2)
            cancel_prob = 0.055 + (0.035 if lead_days > 170 else 0) + (0.025 if channel == "Paid Search" else 0)
            cancelled = RNG.random() < cancel_prob
            cancellation_date = ""
            if cancelled:
                cancellation_date_obj = min(departure - timedelta(days=2), booking_date + timedelta(days=int(RNG.integers(7, max(8, lead_days)))))
                cancellation_date = cancellation_date_obj.isoformat()
                status = "cancelled"
            else:
                status = "completed" if return_date < AS_OF_DATE else "confirmed"
            reservation_id = f"R{res_num:07d}"
            updated_at = cancellation_date or (return_date.isoformat() if status == "completed" else booking_date.isoformat())
            reservations.append(
                {
                    "reservation_id": reservation_id,
                    "guest_id": choice(guest_ids),
                    "sailing_id": sailing.sailing_id,
                    "cabin_id": cabin_id,
                    "booking_date": booking_date.isoformat(),
                    "booking_status": status,
                    "cancellation_date": cancellation_date,
                    "booking_channel": channel,
                    "campaign_id": campaign_id,
                    "passenger_count": passenger_count,
                    "gross_booking_amount": round(gross, 2),
                    "discount_amount": discount,
                    "net_booking_amount": net,
                    "currency": "USD",
                    "updated_at": updated_at,
                }
            )
            deposit = round(net * 0.20, 2)
            payments.append({"payment_id": f"P{pay_num:08d}", "reservation_id": reservation_id, "payment_type": "deposit", "payment_date": booking_date.isoformat(), "payment_amount": deposit, "payment_status": "posted"})
            pay_num += 1
            final_date = max(booking_date + timedelta(days=1), departure - timedelta(days=60))
            if final_date >= departure:
                final_date = departure - timedelta(days=1)
            if cancelled:
                penalty = round(net * (0.12 if (departure - date.fromisoformat(cancellation_date)).days < 60 else 0.06), 2)
                refund = round(-(deposit - penalty), 2)
                payments.append({"payment_id": f"P{pay_num:08d}", "reservation_id": reservation_id, "payment_type": "cancellation_penalty", "payment_date": cancellation_date, "payment_amount": penalty, "payment_status": "posted"})
                pay_num += 1
                if refund < 0:
                    payments.append({"payment_id": f"P{pay_num:08d}", "reservation_id": reservation_id, "payment_type": "refund", "payment_date": cancellation_date, "payment_amount": refund, "payment_status": "posted"})
                    pay_num += 1
            else:
                payments.append({"payment_id": f"P{pay_num:08d}", "reservation_id": reservation_id, "payment_type": "final_payment", "payment_date": final_date.isoformat(), "payment_amount": round(net - deposit, 2), "payment_status": "posted"})
                pay_num += 1
                if return_date < AS_OF_DATE and RNG.random() < 0.62:
                    for cat in RNG.choice(["Spa", "Dining", "Excursion", "Retail", "Beverage"], size=int(RNG.integers(1, 4)), replace=False):
                        onboard.append(
                            {
                                "onboard_spend_id": f"OS{spend_num:08d}",
                                "reservation_id": reservation_id,
                                "service_category": cat,
                                "spend_amount": round(float(RNG.uniform(80, 950) * passenger_count), 2),
                                "spend_date": (departure + timedelta(days=int(RNG.integers(1, max(2, itin["duration_days"]))))).isoformat(),
                            }
                        )
                        spend_num += 1
            res_num += 1
    return pd.DataFrame(reservations), pd.DataFrame(payments), pd.DataFrame(onboard)


def make_aop_targets(sailings, ships, itineraries):
    enriched = sailings.merge(ships[["ship_id", "ship_class"]], on="ship_id").merge(
        itineraries[["itinerary_id", "region", "duration_days", "base_price_multiplier"]], on="itinerary_id"
    )
    months = pd.date_range("2024-01-01", "2026-12-01", freq="MS")
    regions = sorted(itineraries["region"].unique())
    ship_classes = sorted(ships["ship_class"].unique())
    rows = []
    for month in months:
        for region in regions:
            for ship_class in ship_classes:
                related = enriched[
                    (pd.to_datetime(enriched["departure_date"]).dt.to_period("M") == month.to_period("M"))
                    & (enriched["region"] == region)
                    & (enriched["ship_class"] == ship_class)
                ]
                sailings_count = max(1, len(related))
                class_factor = {"Expedition": 1.30, "Ocean": 1.15, "River": 0.92, "Yacht": 1.55}[ship_class]
                region_factor = {
                    "Mediterranean": 1.24,
                    "Alaska": 1.16,
                    "Asia Pacific": 1.20,
                    "Caribbean": 1.02,
                    "European Rivers": 0.96,
                    "Northern Europe": 1.05,
                }[region]
                target = sailings_count * 900000 * class_factor * region_factor * float(RNG.uniform(0.92, 1.08))
                rows.append(
                    {
                        "target_month": month.date().isoformat(),
                        "region": region,
                        "ship_class": ship_class,
                        "revenue_target": round(target, 2),
                        "occupancy_target": round(float(RNG.uniform(0.72, 0.89)), 4),
                        "booking_target": int(sailings_count * RNG.integers(45, 95)),
                    }
                )
    return pd.DataFrame(rows)


def main() -> None:
    ships = make_ships()
    cabins = make_cabins(ships)
    itineraries = make_itineraries()
    guests = make_guests()
    sailings = make_sailings(ships, itineraries)
    campaigns = make_campaigns(itineraries)
    reservations, payments, onboard_spend = make_reservations_and_payments(guests, ships, cabins, itineraries, sailings, campaigns)
    aop_targets = make_aop_targets(sailings, ships, itineraries)
    for name, df in [
        ("guests", guests),
        ("ships", ships),
        ("cabins", cabins),
        ("itineraries", itineraries),
        ("sailings", sailings),
        ("reservations", reservations),
        ("payments", payments),
        ("marketing_campaigns", campaigns),
        ("aop_targets", aop_targets),
        ("onboard_spend", onboard_spend),
    ]:
        save(df, name)
    print(f"Generated {len(reservations):,} reservations, {len(payments):,} payments, {len(sailings):,} sailings.")


if __name__ == "__main__":
    main()
