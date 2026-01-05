import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "app/data/fleetops.db"

LANES = ["PHX-LA", "PHX-SD", "PHX-LV", "PHX-DEN", "PHX-TUC"]

def create_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS shipments (
        shipment_id TEXT PRIMARY KEY,
        pickup_date TEXT,
        delivery_date TEXT,
        planned_delivery_date TEXT,
        miles INTEGER,
        revenue REAL,
        lane TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

def seed_shipments(count=1000):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    base_date = datetime.now() - timedelta(days=90)

    for i in range(count):
        pickup = base_date + timedelta(days=random.randint(0, 90))
        planned = pickup + timedelta(hours=random.randint(12, 48))

        is_late = random.random() < 0.18
        delivery = planned + timedelta(hours=random.randint(1, 12)) if is_late else planned

        miles = random.randint(200, 900)
        revenue = round(miles * random.uniform(1.7, 2.5), 2)

        cur.execute("""
        INSERT OR REPLACE INTO shipments VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"SHP-{i:05d}",
            pickup.isoformat(),
            delivery.isoformat(),
            planned.isoformat(),
            miles,
            revenue,
            random.choice(LANES),
            "delivered"
        ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
    seed_shipments()
    print("✅ Synthetic fleet data created")
