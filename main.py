import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    """Create and return a PostgreSQL connection using DATABASE_URL (Neon)."""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is missing. Set it in .env (local) or Streamlit Secrets (cloud).")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        raise RuntimeError(f"Database connection failed: {e}")






