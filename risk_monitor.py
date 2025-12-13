from main import get_connection


def check_risk_alerts():
    # 1. Connect to database
    conn = get_connection()
    cur = conn.cursor()

    # 2. Query ONLY HIGH RISK alerts from the VIEW
    sql = """
        SELECT home_team, away_team, outcome, exposure, risk_level
        FROM risk_alerts
        WHERE risk_level = 'HIGH RISK'
        ORDER BY exposure DESC;
    """
    cur.execute(sql)
    alerts = cur.fetchall()

    print("\n🚨 HIGH RISK ALERTS 🚨\n")

    # 3. If no high-risk alerts, say everything is OK
    if not alerts:
        print("✅ No HIGH RISK markets at the moment.")
    else:
        for home_team, away_team, outcome, exposure, risk_level in alerts:
            print(
                f"{home_team} vs {away_team} | "
                f"Outcome: {outcome} | "
                f"Exposure: £{exposure:.2f} | "
                f"Risk: {risk_level}"
            )

    # 4. Close connection
    cur.close()
    conn.close()


if __name__ == "__main__":
    check_risk_alerts()
