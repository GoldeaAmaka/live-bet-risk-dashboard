# Live Bet Risk Monitoring Dashboard

A real-time risk monitoring system that simulates live betting activity, calculates exposure (payout risk), and visualises HIGH / MEDIUM / LOW risk alerts using an interactive Streamlit dashboard.

**Live Demo**:  
https://live-bet-risk-dashboard-bbqgzn24yaz9tp9xmp24re.streamlit.app

---

## Project Overview

This project demonstrates how a betting risk team could monitor live market exposure in real time.

It simulates:
- Live betting updates
- Rapid changes in stake and odds
- Risk classification based on potential payout exposure

The system automatically updates and highlights high-risk betting markets to support operational risk decisions.

---

## Key Features

- **Live Simulation Engine**
  - Randomly updates existing bets every few seconds
  - Simulates realistic betting volatility

-  **Risk Classification Logic**
  - LOW / MEDIUM / HIGH risk levels based on payout thresholds

- **Interactive Streamlit Dashboard**
  - Auto-refreshing every 10 seconds
  - KPIs (highest exposure, risk count)
  - Risk table and exposure bar chart

- **PostgreSQL Backend**
  - Structured relational schema
  - Database views for clean analytics

---

## Tech Stack

- **Python**
- **PostgreSQL**
- **Streamlit**
- **Pandas**
- **psycopg2**
- **dotenv**
- **Git & GitHub**

---

## Project Structure

```text
.
├── Dashboard.py        # Streamlit dashboard (frontend)
├── main.py             # Database connection logic
├── simulate_bets.py    # Live bet update simulator
├── risk_monitor.py     # Risk alert querying logic
├── seed_events.py      # Seed initial events
├── seed_markets.py     # Seed betting markets
├── requirements.txt    # Dependencies
└── .gitignore
