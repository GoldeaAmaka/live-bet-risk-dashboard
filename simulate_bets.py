import time
import random
from main import get_connection

UPDATE_EVERY_SECONDS = 10
UPDATE_COUNT = 5 # update 2 existing bets each cycle

def get_existing_bet_ids(conn, limit=500):
    """Fetch a pool of bet_ids to update (limit keeps it fast)."""
    with conn.cursor() as cur:
        cur.execute("SELECT bet_id FROM bets ORDER BY bet_id DESC LIMIT %s;", (limit,))
        rows = cur.fetchall()
    return [r[0] for r in rows]

def update_random_bets():
    conn = get_connection()
    try:
        bet_ids = get_existing_bet_ids(conn, limit=500)

        if len(bet_ids) < UPDATE_COUNT:
            print("Not enough bets to update. Seed bets first.")
            return

        chosen_ids = random.sample(bet_ids, UPDATE_COUNT)

        with conn.cursor() as cur:
            for bet_id in chosen_ids:
                new_stake = round(random.uniform(50, 1500), 2)
                new_odds = round(random.uniform(1.5, 12.0), 2)

                cur.execute(
                    """
                    UPDATE bets
                    SET stake = %s, odds = %s
                    WHERE bet_id = %s;
                    """,
                    (new_stake, new_odds, bet_id),
                )

        conn.commit()
        print(f"Updated {UPDATE_COUNT} bets: {chosen_ids}")

    finally:
        conn.close()

if __name__ == "__main__":
    while True:
        update_random_bets()
        time.sleep(UPDATE_EVERY_SECONDS)
