import os
import sys

# Add backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.db.session import engine, Base
from app.db.models import RationCard, MonthlyAllocation, GrievanceCase, IvrSession, FpsRiskScore, User

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    init_db()
