import os
import sys
import uuid
from datetime import date, datetime
import json

# Add backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.db.session import SessionLocal
from app.db.models import RationCard, MonthlyAllocation, User, FpsRiskScore, GrievanceCase
from app.core.encryption import encryption_service

def seed():
    db = SessionLocal()
    try:
        # 1. Create Demo Official
        h = encryption_service.hash_for_lookup("9988776655")
        u = db.query(User).filter(User.phone_hash == h).first()
        if not u:
            u = User(
                phone_hash=h,
                phone_encrypted=encryption_service.encrypt("9988776655"),
                name="Vikram Singh",
                role="block_official",
                district_code="RJ-BA",
                block_code="RJ-BA-001"
            )
            db.add(u)
            print("Added demo official user")

        # 2. Seed Ration Cards and Allocations from fixtures
        with open(os.path.join(os.path.dirname(__file__), "../../mock_data/epds_fixtures.json"), "r") as f:
            data = json.load(f)

        for rc_data in data["ration_cards"]:
            rc = db.query(RationCard).filter(RationCard.card_number == rc_data["card_number"]).first()
            if not rc:
                rc = RationCard(
                    card_number=rc_data["card_number"],
                    state_code=rc_data["state_code"],
                    district_code=rc_data["district_code"],
                    block_code=rc_data["block_code"],
                    fps_code=rc_data["fps_code"],
                    category=rc_data["category"],
                    household_head_name=encryption_service.encrypt(rc_data["household_head_name"]),
                    total_members=rc_data["total_members"],
                    phone_hash=encryption_service.hash_for_lookup("900000000" + rc_data["card_number"][-1]),
                    phone_encrypted=encryption_service.encrypt("900000000" + rc_data["card_number"][-1]),
                    is_active=rc_data["is_active"],
                    aadhaar_seeded=rc_data["aadhaar_seeded"]
                )
                db.add(rc)
                db.flush()
                print(f"Added ration card: {rc.card_number}")

        for al_data in data["monthly_allocations"]:
            rc = db.query(RationCard).filter(RationCard.card_number == al_data["ration_card_number"]).first()
            if rc:
                dt = datetime.strptime(al_data["month_year"], "%Y-%m-%d").date()
                al = db.query(MonthlyAllocation).filter(
                    MonthlyAllocation.ration_card_id == rc.id,
                    MonthlyAllocation.month_year == dt
                ).first()
                if not al:
                    al = MonthlyAllocation(
                        ration_card_id=rc.id,
                        month_year=dt,
                        rice_kg=al_data["rice_kg"],
                        wheat_kg=al_data["wheat_kg"],
                        sugar_kg=al_data["sugar_kg"],
                        fps_code=al_data["fps_code"]
                    )
                    db.add(al)
                    print(f"Added allocation for {rc.card_number}")

        # 3. Seed some FPS Risk Scores
        fps_codes = ["RJ-BA-001", "RJ-BA-003", "RJ-BA-004", "RJ-BA-005"]
        for code in fps_codes:
            f = db.query(FpsRiskScore).filter(FpsRiskScore.fps_code == code).first()
            if not f:
                f = FpsRiskScore(
                    fps_code=code,
                    district_code="RJ-BA",
                    block_code="RJ-BA-001" if code == "RJ-BA-001" else "RJ-BA-002",
                    fps_name=f"Fair Price Shop {code[-3:]}",
                    composite_risk_score=45.5 if code == "RJ-BA-001" else 12.0,
                    risk_tier="high" if code == "RJ-BA-001" else "low"
                )
                db.add(f)
                print(f"Added FPS Risk Score: {code}")

        # 4. Seed a few grievances
        rc = db.query(RationCard).first()
        if rc:
            gc = db.query(GrievanceCase).filter(GrievanceCase.ration_card_id == rc.id).first()
            if not gc:
                gc = GrievanceCase(
                    case_number="RS-RJ-2025-00001",
                    ration_card_id=rc.id,
                    reporter_type="self",
                    fps_code=rc.fps_code,
                    district_code=rc.district_code,
                    block_code=rc.block_code,
                    issue_type="short_supply",
                    reported_month_year=date(2025, 10, 1),
                    expected_wheat_kg=5.0,
                    received_wheat_kg=2.0,
                    status="open"
                )
                db.add(gc)
                print(f"Added sample grievance: {gc.case_number}")

        db.commit()
        print("Seeding completed successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
