from sqlalchemy import func

from app.database import SessionLocal
from app.models.load import Load

db = SessionLocal()


def total_revenue():

    revenue = db.query(
        func.sum(Load.revenue)
    ).scalar()

    return {
        "total_revenue": round(float(revenue or 0), 2)
    }


def average_revenue():

    avg = db.query(
        func.avg(Load.revenue)
    ).scalar()

    return {
        "average_revenue": round(avg, 2)
    }


def total_loaded_miles():

    miles = db.query(
        func.sum(Load.loaded_miles)
    ).scalar()

    return {
        "total_loaded_miles": round(miles, 2)
    }


def total_empty_miles():

    miles = db.query(
        func.sum(Load.empty_miles)
    ).scalar()

    return {
        "total_empty_miles": round(miles, 2)
    }
    
    
def top_customers():

    rows = db.query(
        Load.customer,
        func.sum(Load.revenue)
    ).group_by(
        Load.customer
    ).order_by(
        func.sum(Load.revenue).desc()
    ).limit(5).all()

    return [
        {
            "customer": r[0],
            "revenue": round(r[1], 2)
        }
        for r in rows
    ]  
    
    
def top_routes():

    rows = db.query(
        Load.origin,
        Load.destination,
        func.sum(Load.revenue)
    ).group_by(
        Load.origin,
        Load.destination
    ).order_by(
        func.sum(Load.revenue).desc()
    ).limit(5).all()

    return [
        {
            "route": f"{r[0]} → {r[1]}",
            "revenue": round(r[2], 2)
        }
        for r in rows
    ] 
    
    
def delayed_loads():

    count = db.query(
        func.count()
    ).filter(
        Load.status == "Delayed"
    ).scalar()

    return {
        "delayed_loads": count
    }         