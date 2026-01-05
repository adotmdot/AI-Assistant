import sqlite3
from datetime import datetime, timedelta

DB_PATH = "app/data/fleetops.db"

def on_time_percentage(days=7):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    start = datetime.now() - timedelta(days=days)

    cur.execute("""
        SELECT 
            COUNT(*) AS total,
            SUM(CASE WHEN delivery_date <= planned_delivery_date THEN 1 ELSE 0 END) AS on_time
        FROM shipments
        WHERE pickup_date >= ?
    """, (start.isoformat(),))

    total, on_time = cur.fetchone()
    conn.close()

    if not total:
        return None

    return round((on_time / total) * 100, 2)
