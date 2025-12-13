import psycopg2
from psycopg2.extras import RealDictCursor

import os
from dotenv import load_dotenv


load_dotenv()
MY_PASSWORD = os.getenv("My_password")

def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="live_bet_monitoring_system",
            user="postgres",
            password=MY_PASSWORD,
            port=5432
        )
        print("Connected successfully!")
        return conn
    except Exception as e:
        print("Error connecting to PostgreSQL:", e)

conn = get_connection()
print(conn)




