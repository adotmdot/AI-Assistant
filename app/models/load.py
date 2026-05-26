from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

class Load(Base):
    __tablename__ = "loads"

    id = Column(Integer, primary_key=True, index=True)

    customer = Column(String)
    origin = Column(String)
    destination = Column(String)

    revenue = Column(Float)

    loaded_miles = Column(Float)
    empty_miles = Column(Float)

    status = Column(String)

    delivery_date = Column(Date)