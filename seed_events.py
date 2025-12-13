from main import get_connection


def seed_events():
    seeding = [
    {
        "home_team": "Barcelona",
        "away_team": "chelsea",
        "start_time": "2025-12-01 20:00:00",
        "competition": "premier league"
    },

    {
        "home_team": "Manchester United",
        "away_team": "Arsenal",
        "start_time": "2025-12-02 18:30:00",
        "competition": "Premier League"
    },
    {
        "home_team": "Real Madrid",
        "away_team": "Atletico Madrid",
        "start_time": "2025-12-03 21:00:00",
        "competition": "La Liga"
    },
    {
        "home_team": "Bayern Munich",
        "away_team": "Borussia Dortmund",
        "start_time": "2025-12-04 19:45:00",
        "competition": "Bundesliga"
    },
    {
        "home_team": "PSG",
        "away_team": "Marseille",
        "start_time": "2025-12-05 20:15:00",
        "competition": "Ligue 1"
    }

]

    conn = get_connection()
    cur=conn.cursor()

    insert_sql = """
           INSERT INTO events (home_team, away_team, start_time, competition)
           VALUES (%s, %s, %s, %s);
       """
    for match in seeding:
        cur.execute(insert_sql, (
            match["home_team"],
            match["away_team"],
            match["start_time"],
            match["competition"]
        ))

    # 5. Save changes & close everything
    conn.commit()
    cur.close()
    conn.close()

    print("1 event inserted successfully!")


if __name__ == "__main__":
    seed_events()

