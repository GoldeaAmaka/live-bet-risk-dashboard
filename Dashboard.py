import os
import pandas as pd
import streamlit as st
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env (local dev)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
REFRESH_SECONDS = 10  # refresh every 10 seconds


def get_connection():
    try:
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL is missing. Add it to your .env file or Streamlit Secrets.")
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None


def classify_risk(payouts: float) -> str:
    # Adjust these thresholds to fit your story/demo
    if payouts >= 1000:
        return "HIGH RISK"
    elif payouts >= 400:
        return "MEDIUM RISK"
    else:
        return "LOW RISK"


def load_risk_dashboard():
    conn = get_connection()
    if conn is None:
        st.stop()

    try:
        with conn.cursor() as cur:
            # We still read "exposure" from the DB view,
            # but we present it as "payouts" to users.
            sql = """
                SELECT home_team, away_team, outcome, exposure
                FROM public.risk_dashboard
                ORDER BY exposure DESC;
            """
            cur.execute(sql)
            rows = cur.fetchall()

        df = pd.DataFrame(rows, columns=["home_team", "away_team", "outcome", "payouts"])

        if df.empty:
            df["risk_level"] = []
            return df

        df["risk_level"] = df["payouts"].apply(classify_risk)
        return df

    except Exception as e:
        st.error(f"Database error: {e}")
        st.stop()
    finally:
        conn.close()


# ---- PAGE CONFIG ----
st.set_page_config(page_title="Real-Time Risk Alerts Dashboard", layout="wide")

# ✅ Auto-refresh
st.markdown(
    f"<meta http-equiv='refresh' content='{REFRESH_SECONDS}'>",
    unsafe_allow_html=True
)

st.title("📊 Real-Time Risk Alerts Dashboard")
st.caption("Auto-refreshing every 10 seconds. Shows potential payout exposure and risk level.")

df = load_risk_dashboard()

# ---- KPI ROW ----
col1, col2, col3, col4 = st.columns(4)

total_rows = len(df)
max_payout = float(df["payouts"].max()) if total_rows > 0 else 0.0
high_count = int((df["risk_level"] == "HIGH RISK").sum()) if total_rows > 0 else 0
med_count = int((df["risk_level"] == "MEDIUM RISK").sum()) if total_rows > 0 else 0
low_count = int((df["risk_level"] == "LOW RISK").sum()) if total_rows > 0 else 0

col1.metric("Rows monitored", total_rows)
col2.metric("Highest potential payout", f"£{max_payout:,.2f}")
col3.metric("HIGH risk", high_count)
col4.metric("MEDIUM risk", med_count)

st.divider()

# ---- FILTERS ----
left, right = st.columns([2, 1])
with right:
    risk_filter = st.multiselect(
        "Filter risk levels",
        ["HIGH RISK", "MEDIUM RISK", "LOW RISK"],
        default=["HIGH RISK", "MEDIUM RISK", "LOW RISK"],
    )

filtered = df.copy()
if total_rows > 0:
    filtered = filtered[filtered["risk_level"].isin(risk_filter)]

# ---- SUMMARY STRIP ----
if total_rows > 0:
    st.write(
        f"**Breakdown:** HIGH = {high_count} • MEDIUM = {med_count} • LOW = {low_count}"
    )

# ---- TABLE ----
st.subheader("Top Risk Alerts (sorted by potential payout)")
if filtered.empty:
    st.info("No rows match your filter yet.")
else:
    display_df = filtered.head(20).copy()
    display_df["payouts"] = display_df["payouts"].map(lambda x: f"£{x:,.2f}")
    display_df = display_df.rename(columns={"payouts": "potential_payout"})
    st.dataframe(display_df, use_container_width=True)

st.divider()

# ---- CHART ----
st.subheader("Total potential payout by outcome")
if filtered.empty:
    st.info("No data available for chart yet.")
else:
    chart_df = (
        filtered.groupby("outcome", as_index=False)["payouts"]
        .sum()
        .sort_values("payouts", ascending=False)
    )
    st.bar_chart(chart_df, x="outcome", y="payouts")
