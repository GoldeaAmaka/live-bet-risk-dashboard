import time
from main import get_connection
from datetime import datetime
import random

def simulate():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT market_id, event_id, initial_odds
        FROM markets;
    """)
    markets = cur.fetchall()

    while True:
        for _ in range(2):  # insert 2 bets
            market_id, event_id, odds = random.choice(markets)
            customer_id = random.randint(1, 1500)
            stake = random.randint(5, 10000)

            cur.execute("""
                INSERT INTO bets (event_id, market_id, customer_id, stake, odds)
                VALUES (%s, %s, %s, %s, %s);
            """, (event_id, market_id, customer_id, stake, odds))

        conn.commit()
        print(f"Inserted 2 bets at {datetime.now().strftime('%H:%M:%S')}")
        time.sleep(10)  # wait 10 seconds

simulate()
