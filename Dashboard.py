import pandas as pd
import streamlit as st
from main import get_connection

REFRESH_SECONDS = 10  # refresh every 10 seconds


def load_risk_alerts():
    try:
        conn = get_connection()
        cur = conn.cursor()

        sql = """
            SELECT home_team, away_team, outcome, exposure, risk_level
            FROM risk_alerts
            ORDER BY exposure DESC;
        """
        cur.execute(sql)
        rows = cur.fetchall()

        cur.close()
        conn.close()

        df = pd.DataFrame(
            rows,
            columns=["home_team", "away_team", "outcome", "exposure", "risk_level"]
        )
        return df

    except Exception as e:
        st.error(f"Database error: {e}")
        st.stop()


# ---- PAGE CONFIG ----
st.set_page_config(page_title="Risk Alerts Dashboard", layout="wide")

# ✅ Auto-refresh (works without extra modules)
st.markdown(
    f"<meta http-equiv='refresh' content='{REFRESH_SECONDS}'>",
    unsafe_allow_html=True
)

st.title("📊 Real-Time Risk Alerts Dashboard")
st.caption(f"Auto-refreshing every {REFRESH_SECONDS} seconds...")

df = load_risk_alerts()

# ---- KPI ROW ----
col1, col2, col3 = st.columns(3)

total_rows = len(df)
max_exposure = float(df["exposure"].max()) if total_rows > 0 else 0
high_risk_count = int((df["risk_level"] == "HIGH RISK").sum()) if total_rows > 0 else 0

col1.metric("Rows in risk_alerts", total_rows)
col2.metric("Highest Exposure", f"£{max_exposure:,.2f}")
col3.metric("HIGH RISK Count", high_risk_count)

st.divider()

# ---- TABLE ----
st.subheader("Top Risk Alerts (sorted by exposure)")
if total_rows == 0:
    st.info("No rows found in risk_alerts yet.")
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
