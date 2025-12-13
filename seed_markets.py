from main import get_connection


def seed_markets():
    # 1. Connect to the database
    conn = get_connection()
    cur = conn.cursor()

    # 2. Get all events (matches)
    cur.execute("SELECT event_id, home_team, away_team FROM events;")
    events = cur.fetchall()   # list of tuples like (event_id, home_team, away_team)

    # 3. SQL for inserting markets
    insert_sql = """
        INSERT INTO markets (event_id, market_name, outcome, initial_odds)
        VALUES (%s, %s, %s, %s);
    """

    # 4. For each event, create 3 Match Result outcomes
    for event_id, home_team, away_team in events:
        # Home team to win
        cur.execute(insert_sql, (
            event_id,
            "Match Result",           # market_name
            f"{home_team} Win",       # outcome
            1.80                      # example odds
        ))

        # Draw
        cur.execute(insert_sql, (
            event_id,
            "Match Result",
            "Draw",
            3.40
        ))

        # Away team to win
        cur.execute(insert_sql, (
            event_id,
            "Match Result",
            f"{away_team} Win",
            2.60
        ))

    # 5. Save and close
    conn.commit()
    cur.close()
    conn.close()

    print(f"{len(events) * 3} markets inserted successfully!")



if __name__ == "__main__":
    seed_markets()