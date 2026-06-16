from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TABLEAU = ROOT / "dashboards" / "tableau" / "exported_extracts"
POWERBI = ROOT / "dashboards" / "powerbi" / "exported_extracts"
SCREENSHOTS = ROOT / "docs" / "screenshots"


def money(value: float) -> str:
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    return f"${value / 1_000:.0f}K"


def dollars(value: float) -> str:
    return f"${value:,.0f}"


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def style_axis(ax, title: str) -> None:
    ax.set_title(title, loc="left", fontsize=13, fontweight="bold", pad=10)
    ax.grid(axis="y", color="#D9DEE7", linewidth=0.8)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="both", labelsize=9)


def generate_tableau_scorecard() -> None:
    score = pd.read_csv(TABLEAU / "mart_executive_scorecard.csv", parse_dates=["month_start"])
    revenue = pd.read_csv(TABLEAU / "fct_revenue_recognition.csv", parse_dates=["recognition_month"])
    occupancy = pd.read_csv(TABLEAU / "fct_occupancy_daily.csv", parse_dates=["month_start"])
    booking = pd.read_csv(TABLEAU / "fct_booking_daily.csv", parse_dates=["booking_month"])
    revenue_mgmt = pd.read_csv(TABLEAU / "mart_revenue_management.csv", parse_dates=["departure_date"])

    latest_month = score.loc[score["recognized_revenue"] > 0, "month_start"].max()
    if pd.isna(latest_month):
        latest_month = score["month_start"].max()
    current = score[score["month_start"] == latest_month].copy()

    fig = plt.figure(figsize=(20, 11), facecolor="#F6F8FB")
    gs = fig.add_gridspec(3, 3, height_ratios=[0.55, 1.25, 1.25], hspace=0.55, wspace=0.42)
    fig.suptitle("Luxury Cruise Executive Scorecard", x=0.03, y=0.98, ha="left", fontsize=24, fontweight="bold", color="#1F2937")
    fig.text(0.03, 0.945, f"Reporting month: {latest_month:%Y-%m} | Governed dbt marts for revenue, occupancy, pace, and cancellation risk", fontsize=11, color="#4B5563")

    kpi_ax = fig.add_subplot(gs[0, :])
    kpi_ax.axis("off")
    kpis = [
        ("Recognized Revenue", money(current["recognized_revenue"].sum())),
        ("Revenue AOP", money(current["revenue_target"].sum())),
        ("AOP Attainment", pct(current["recognized_revenue"].sum() / current["revenue_target"].sum())),
        ("Occupancy", pct((current["occupancy_rate"] * current["booking_target"]).sum() / current["booking_target"].sum())),
        ("Bookings", f"{int(current['bookings'].sum()):,}"),
        ("Revenue / Pax Night", money(revenue["revenue_per_passenger_night"].replace([np.inf, -np.inf], np.nan).dropna().mean())),
    ]
    for i, (label, value) in enumerate(kpis):
        x = 0.01 + i * 0.162
        card = plt.Rectangle((x, 0.08), 0.145, 0.74, transform=kpi_ax.transAxes, facecolor="white", edgecolor="#D8DEE9", linewidth=1.1)
        kpi_ax.add_patch(card)
        kpi_ax.text(x + 0.018, 0.56, value, transform=kpi_ax.transAxes, fontsize=18, fontweight="bold", color="#0F172A")
        kpi_ax.text(x + 0.018, 0.30, label, transform=kpi_ax.transAxes, fontsize=9.5, color="#64748B")

    ax1 = fig.add_subplot(gs[1, 0])
    rev_region = current.groupby("region", as_index=False)[["recognized_revenue", "revenue_target"]].sum().sort_values("recognized_revenue")
    y = np.arange(len(rev_region))
    ax1.barh(y - 0.18, rev_region["revenue_target"] / 1_000_000, height=0.34, color="#CBD5E1", label="AOP")
    ax1.barh(y + 0.18, rev_region["recognized_revenue"] / 1_000_000, height=0.34, color="#2563EB", label="Actual")
    ax1.set_yticks(y, rev_region["region"])
    ax1.set_xlabel("Revenue ($M)")
    ax1.legend(frameon=False, fontsize=9)
    style_axis(ax1, "Revenue vs AOP by Region")

    ax2 = fig.add_subplot(gs[1, 1])
    occ = occupancy.groupby(["region", "ship_class"], as_index=False).agg({"sold_passenger_nights": "sum", "available_passenger_nights": "sum"})
    occ["occupancy_rate"] = occ["sold_passenger_nights"] / occ["available_passenger_nights"]
    pivot = occ.pivot(index="region", columns="ship_class", values="occupancy_rate").fillna(0)
    im = ax2.imshow(pivot.values, cmap="YlGnBu", vmin=0, vmax=max(1.0, pivot.values.max()))
    ax2.set_xticks(np.arange(len(pivot.columns)), pivot.columns, rotation=25, ha="right")
    ax2.set_yticks(np.arange(len(pivot.index)), pivot.index)
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            ax2.text(j, i, pct(pivot.iloc[i, j]), ha="center", va="center", fontsize=8, color="#0F172A")
    ax2.set_title("Occupancy by Region and Ship Class", loc="left", fontsize=12.5, fontweight="bold", pad=10)
    fig.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)

    ax3 = fig.add_subplot(gs[1, 2])
    bucket_order = ["180+ days", "120-179 days", "90-119 days", "60-89 days", "30-59 days", "0-29 days"]
    pace = booking.groupby("lead_time_bucket", as_index=False)["bookings"].sum()
    pace["lead_time_bucket"] = pd.Categorical(pace["lead_time_bucket"], categories=bucket_order, ordered=True)
    pace = pace.sort_values("lead_time_bucket")
    ax3.plot(pace["lead_time_bucket"].astype(str), pace["bookings"], marker="o", color="#7C3AED", linewidth=2.5)
    ax3.tick_params(axis="x", rotation=30)
    ax3.set_ylabel("Bookings")
    style_axis(ax3, "Booking Pace by Lead Time")

    ax4 = fig.add_subplot(gs[2, 0])
    under = revenue_mgmt.sort_values("occupancy_gap", ascending=False).head(10).sort_values("occupancy_gap")
    ax4.barh(under["sailing_id"], under["occupancy_gap"], color="#F97316")
    ax4.set_xlabel("Occupancy Gap")
    ax4.xaxis.set_major_formatter(lambda x, pos: pct(x))
    style_axis(ax4, "Top Underperforming Sailings")

    ax5 = fig.add_subplot(gs[2, 1])
    channel = booking.groupby("booking_channel", as_index=False)[["cancellations", "bookings"]].sum()
    channel["cancellation_rate"] = channel["cancellations"] / channel["bookings"]
    channel = channel.sort_values("cancellation_rate")
    ax5.barh(channel["booking_channel"], channel["cancellation_rate"], color="#DC2626")
    ax5.set_xlabel("Cancellation Rate")
    ax5.xaxis.set_major_formatter(lambda x, pos: pct(x))
    style_axis(ax5, "Cancellation Rate by Booking Channel")

    ax6 = fig.add_subplot(gs[2, 2])
    rppn = revenue.groupby("region", as_index=False).agg({"recognized_revenue": "sum", "sold_passenger_nights": "sum"})
    rppn["revenue_per_passenger_night"] = rppn["recognized_revenue"] / rppn["sold_passenger_nights"]
    rppn = rppn.sort_values("revenue_per_passenger_night")
    ax6.barh(rppn["region"], rppn["revenue_per_passenger_night"], color="#059669")
    ax6.set_xlabel("Revenue / Passenger Night")
    ax6.xaxis.set_major_formatter(lambda x, pos: dollars(x))
    style_axis(ax6, "Revenue per Passenger Night")

    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    fig.savefig(SCREENSHOTS / "tableau_executive_scorecard.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def generate_powerbi_finance() -> None:
    wf = pd.read_csv(POWERBI / "mart_finance_revenue_waterfall_monthly.csv", parse_dates=["accounting_month"])
    finance = pd.read_csv(POWERBI / "mart_finance_revenue.csv", parse_dates=["recognition_month"])
    recent = wf[wf["accounting_month"] >= wf["accounting_month"].max() - pd.DateOffset(months=11)].copy()
    monthly = recent.groupby("accounting_month", as_index=False)[["beginning_deferred_revenue", "cash_collected", "refunds", "cancellation_penalties", "recognized_revenue", "ending_deferred_revenue"]].sum()

    fig = plt.figure(figsize=(16, 9), facecolor="#F7F7F8")
    gs = fig.add_gridspec(2, 2, height_ratios=[0.7, 1.4], hspace=0.4, wspace=0.25)
    fig.suptitle("Finance Revenue Recognition / Deferred Revenue Waterfall", x=0.03, y=0.97, ha="left", fontsize=22, fontweight="bold", color="#111827")
    fig.text(0.03, 0.93, "Power BI-style finance proof: cash activity, refunds, penalties, recognition, and deferred revenue roll-forward", fontsize=10.5, color="#4B5563")

    kpi_ax = fig.add_subplot(gs[0, :])
    kpi_ax.axis("off")
    kpis = [
        ("Ending Deferred", money(monthly["ending_deferred_revenue"].iloc[-1])),
        ("Cash Collected", money(monthly["cash_collected"].sum())),
        ("Refund Exposure", money(finance["refund_exposure"].sum())),
        ("Cancellation Penalties", money(monthly["cancellation_penalties"].sum())),
        ("Recognized Revenue", money(monthly["recognized_revenue"].sum())),
    ]
    for i, (label, value) in enumerate(kpis):
        x = 0.015 + i * 0.19
        card = plt.Rectangle((x, 0.18), 0.17, 0.62, transform=kpi_ax.transAxes, facecolor="white", edgecolor="#D1D5DB")
        kpi_ax.add_patch(card)
        kpi_ax.text(x + 0.016, 0.58, value, transform=kpi_ax.transAxes, fontsize=17, fontweight="bold", color="#111827")
        kpi_ax.text(x + 0.016, 0.36, label, transform=kpi_ax.transAxes, fontsize=9.5, color="#6B7280")

    ax1 = fig.add_subplot(gs[1, 0])
    x = np.arange(len(monthly))
    ax1.bar(x, monthly["cash_collected"] / 1_000_000, label="Cash collected", color="#2563EB")
    ax1.bar(x, monthly["cancellation_penalties"] / 1_000_000, bottom=monthly["cash_collected"] / 1_000_000, label="Penalties", color="#10B981")
    ax1.bar(x, monthly["refunds"] / 1_000_000, label="Refunds", color="#EF4444")
    ax1.plot(x, monthly["recognized_revenue"] / 1_000_000, color="#111827", linewidth=2.5, marker="o", label="Recognized revenue")
    ax1.set_xticks(x, monthly["accounting_month"].dt.strftime("%Y-%m"), rotation=45, ha="right")
    ax1.set_ylabel("$M")
    ax1.legend(frameon=False, fontsize=9)
    style_axis(ax1, "Monthly Cash Activity and Recognition")

    ax2 = fig.add_subplot(gs[1, 1])
    ax2.plot(x, monthly["beginning_deferred_revenue"] / 1_000_000, marker="o", label="Beginning deferred", color="#7C3AED")
    ax2.plot(x, monthly["ending_deferred_revenue"] / 1_000_000, marker="o", label="Ending deferred", color="#F97316")
    ax2.fill_between(x, monthly["beginning_deferred_revenue"] / 1_000_000, monthly["ending_deferred_revenue"] / 1_000_000, color="#FDBA74", alpha=0.25)
    ax2.set_xticks(x, monthly["accounting_month"].dt.strftime("%Y-%m"), rotation=45, ha="right")
    ax2.set_ylabel("$M")
    ax2.legend(frameon=False, fontsize=9)
    style_axis(ax2, "Deferred Revenue Roll-Forward")

    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    fig.savefig(SCREENSHOTS / "powerbi_finance_revenue_waterfall.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    generate_tableau_scorecard()
    generate_powerbi_finance()
    print("Generated dashboard screenshots in docs/screenshots.")


if __name__ == "__main__":
    main()
