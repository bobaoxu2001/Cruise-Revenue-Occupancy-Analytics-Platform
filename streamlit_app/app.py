from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def load_csv(name: str) -> pd.DataFrame:
    path = PROCESSED / f"{name}.csv"
    if not path.exists():
        st.error(f"Missing {path}. Run dbt build and python scripts/export_bi_extracts.py first.")
        st.stop()
    return pd.read_csv(path)


QUESTIONS = [
    "Which itineraries are below AOP target this month?",
    "What are the top 10 sailings by occupancy gap?",
    "Which booking channels have the highest cancellation rate?",
    "How much deferred revenue is scheduled to recognize next month?",
    "Which campaigns have the best ROAS?",
]


st.set_page_config(page_title="Cruise AI Analyst", layout="wide")
st.title("Luxury Cruise Governed AI Analyst Demo")
question = st.selectbox("Choose a governed question", QUESTIONS)
free_text = st.text_input("Optional natural-language note", placeholder="Example: focus on Mediterranean sailings")

if question == QUESTIONS[0]:
    df = load_csv("mart_executive_scorecard")
    df["month_start"] = pd.to_datetime(df["month_start"])
    month = df["month_start"].max()
    answer = df[(df["month_start"] == month) & (df["revenue_aop_attainment"] < 1)].sort_values("revenue_aop_attainment").head(15)
    st.caption("Metric definition: revenue AOP attainment = recognized revenue / revenue target.")
    st.code("SELECT * FROM mart_executive_scorecard WHERE month_start = max_month AND revenue_aop_attainment < 1 ORDER BY revenue_aop_attainment")
    st.dataframe(answer)
    st.plotly_chart(px.bar(answer, x="region", y="revenue_aop_attainment", color="ship_class"), use_container_width=True)
elif question == QUESTIONS[1]:
    df = load_csv("mart_revenue_management").sort_values("occupancy_gap", ascending=False).head(10)
    st.caption("Metric definition: occupancy gap = 1 - sold passenger nights / available passenger nights.")
    st.code("SELECT sailing_id, itinerary_name, occupancy_gap FROM mart_revenue_management ORDER BY occupancy_gap DESC LIMIT 10")
    st.dataframe(df)
    st.plotly_chart(px.bar(df, x="sailing_id", y="occupancy_gap", color="region"), use_container_width=True)
elif question == QUESTIONS[2]:
    df = load_csv("fct_booking_daily")
    grouped = df.groupby("booking_channel", as_index=False).agg({"cancellations": "sum", "bookings": "sum"})
    grouped["cancellation_rate"] = grouped["cancellations"] / grouped["bookings"]
    grouped = grouped.sort_values("cancellation_rate", ascending=False)
    st.caption("Metric definition: cancellation rate = cancelled bookings / total bookings.")
    st.code("SELECT booking_channel, SUM(cancellations) / SUM(bookings) AS cancellation_rate FROM fct_booking_daily GROUP BY 1")
    st.dataframe(grouped)
    st.plotly_chart(px.bar(grouped, x="booking_channel", y="cancellation_rate"), use_container_width=True)
elif question == QUESTIONS[3]:
    df = load_csv("mart_finance_revenue")
    df["recognition_month"] = pd.to_datetime(df["recognition_month"])
    current = df["recognition_month"].min()
    next_month = current + pd.offsets.MonthBegin(1)
    upcoming = df[df["recognition_month"] == next_month]
    total = upcoming["deferred_revenue"].sum()
    st.metric("Deferred revenue scheduled for selected next month", f"${total:,.0f}")
    st.caption("Metric definition: deferred revenue = cash collected minus recognized revenue where recognition is pending.")
    st.code("SELECT recognition_month, SUM(deferred_revenue) FROM mart_finance_revenue GROUP BY 1 ORDER BY 1")
    st.dataframe(upcoming.sort_values("deferred_revenue", ascending=False).head(20))
elif question == QUESTIONS[4]:
    df = load_csv("mart_marketing_performance")
    answer = df[df["campaign_spend"] > 0].sort_values("campaign_roas", ascending=False).head(15)
    st.caption("Metric definition: campaign ROAS = attributed net booking revenue / campaign spend.")
    st.code("SELECT campaign_name, campaign_roas FROM mart_marketing_performance WHERE campaign_spend > 0 ORDER BY campaign_roas DESC")
    st.dataframe(answer)
    st.plotly_chart(px.bar(answer, x="campaign_name", y="campaign_roas", color="target_region"), use_container_width=True)

if free_text:
    st.info("This demo keeps answers governed by the menu above. The note is captured as business context but does not change SQL logic.")
