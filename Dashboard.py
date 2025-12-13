import os
import pandas as pd
import streamlit as st
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

REFRESH_SECONDS = 10  # refresh every 10 seconds


def get_connection():
    try:
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL is missing. Add it to your .env file.")
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None


def load_risk_dashboard():
    conn = get_connection()
    if conn is None:
        st.stop()

    try:
        with conn.cursor() as cur:
            sql = """
                SELECT home_team, away_team, outcome, exposure
                FROM public.risk_dashboard
                ORDER BY exposure DESC;
            """
            cur.execute(sql)
            rows = cur.fetchall()

        df = pd.DataFrame(rows, columns=["home_team", "away_team", "outcome", "exposure"])

        # Create risk level locally (you can adjust these thresholds)
        def classify_risk(exposure):
            if exposure >= 500:
                return "HIGH RISK"
            elif exposure >= 200:
                return "MEDIUM RISK"
            else:
                return "LOW RISK"

        if not df.empty:
            df["risk_level"] = df["exposure"].apply(classify_risk)
        else:
            df["risk_level"] = []

        return df

    except Exception as e:
        st.error(f"Database error: {e}")
        st.stop()

    finally:
        conn.close()


# ---- PAGE CONFIG ----
st.set_page_config(page_title="Risk Alerts Dashboard", layout="wide")

# ✅ Auto-refresh
st.markdown(
    f"<meta http-equiv='refresh' content='{REFRESH_SECONDS}'>",
    unsafe_allow_html=True
)

st.title("📊 Real-Time Risk Alerts Dashboard")
st.caption(f"Auto-refreshing every {REFRESH_SECONDS} seconds...")

df = load_risk_dashboard()

# ---- KPI ROW ----
col1, col2, col3 = st.columns(3)

total_rows = len(df)
max_exposure = float(df["exposure"].max()) if total_rows > 0 else 0
high_risk_count = int((df["risk_level"] == "HIGH RISK").sum()) if total_rows > 0 else 0

col1.metric("Rows in risk_dashboard", total_rows)
col2.metric("Highest Exposure", f"£{max_exposure:,.2f}")
col3.metric("HIGH RISK Count", high_risk_count)

st.divider()

# ---- TABLE ----
st.subheader("Top Risk Alerts (sorted by exposure)")
if total_rows == 0:
    st.info("No rows found in risk_dashboard yet.")
else:
    st.dataframe(df.head(20), use_container_width=True)

st.divider()

# ---- CHART ----
st.subheader("Exposure by Outcome")
if total_rows > 0:
    chart_df = (
        df.groupby("outcome", as_index=False)["exposure"]
        .sum()
        .sort_values("exposure", ascending=False)
    )
    st.bar_chart(chart_df, x="outcome", y="exposure")
