from main import get_connection


def check_risk_alerts():
    # 1. Connect to database
    conn = get_connection()
    cur = conn.cursor()

    # 2. Query HIGH and MEDIUM risk alerts from the view
    sql = """
        SELECT
            home_team,
            away_team,
            outcome,
            payouts,
            risk_level
        FROM risk_alerts
        WHERE risk_level IN ('HIGH RISK', 'MEDIUM RISK')
        ORDER BY payouts DESC;
    """

    cur.execute(sql)
    alerts = cur.fetchall()

    print("\n🚨 RISK ALERTS (HIGH & MEDIUM) 🚨\n")

    # 3. If no alerts, say everything is OK
    if not alerts:
        print("✅ No HIGH or MEDIUM risk markets at the moment.")
    else:
        for home_team, away_team, outcome, payouts, risk_level in alerts:
            print(
                f"{home_team} vs {away_team} | "
                f"Outcome: {outcome} | "
                f"Potential Payout: £{payouts:,.2f} | "
                f"Risk Level: {risk_level}"
            )

    # 4. Close connection
    cur.close()
    conn.close()


if __name__ == "__main__":
    check_risk_alerts()
