from faker import Faker
from random import choice, randint, uniform
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.models.load import Load

fake = Faker()

db = SessionLocal()

customers = [
    "Walmart",
    "Amazon",
    "Target",
    "Costco",
    "Pepsi",
    "Coca-Cola",
    "Home Depot",
    "Lowes"
]

cities = [
    "Phoenix",
    "Dallas",
    "Atlanta",
    "Chicago",
    "Los Angeles",
    "Houston",
    "Las Vegas",
    "Denver"
]

statuses = [
    "Delivered",
    "In Transit",
    "Delayed",
    "Scheduled"
]

for _ in range(5000):

    origin = choice(cities)

    destination = choice(
        [city for city in cities if city != origin]
    )

    loaded_miles = randint(200, 2500)

    empty_miles = randint(10, 400)

    revenue = round(
        loaded_miles * uniform(1.8, 3.5),
        2
    )

    load = Load(
        customer=choice(customers),
        origin=origin,
        destination=destination,
        revenue=revenue,
        loaded_miles=loaded_miles,
        empty_miles=empty_miles,
        status=choice(statuses),
        delivery_date=datetime.now().date()
        - timedelta(days=randint(0, 90))
    )

    db.add(load)

db.commit()

print("5000 logistics loads inserted.")