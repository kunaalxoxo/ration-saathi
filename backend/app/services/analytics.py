import duckdb, pandas as pd, os; from datetime import datetime, timedelta; from sqlalchemy.orm import Session; from app.db.session import SessionLocal; from app.db.models import GrievanceCase, FpsRiskScore, RationCard, MonthlyAllocation
class AnalyticsService:
    def __init__(self): self.db_path = "data/analytics.duckdb"; os.makedirs("data", exist_ok=True); self.con = duckdb.connect(database=self.db_path, read_only=False)
    def _sync(self, db: Session):
        gr = db.query(GrievanceCase).all(); ca = db.query(RationCard).all(); al = db.query(MonthlyAllocation).all()
        pd.DataFrame([vars(g) for g in gr]).to_parquet("data/grievances.parquet")
        pd.DataFrame([vars(c) for c in ca]).to_parquet("data/cards.parquet")
        pd.DataFrame([vars(a) for a in al]).to_parquet("data/allocations.parquet")
    def calculate_fps_risk_score(self, fps: str):
        db = SessionLocal()
        try:
            self._sync(db); st = self.con.execute(f"SELECT COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '30 days'), COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '90 days'), COUNT(*) FILTER (WHERE status = 'resolved') * 100.0 / NULLIF(COUNT(*), 0), COUNT(DISTINCT ration_card_id) * 1.0 / NULLIF(COUNT(*), 0) FROM 'data/grievances.parquet' WHERE fps_code = '{fps}'").fetchone()
            tot = self.con.execute(f"SELECT COUNT(*) FROM 'data/cards.parquet' WHERE fps_code = '{fps}'").fetchone()[0] or 1
            an = self.con.execute(f"SELECT AVG(CASE WHEN actual_offtake_wheat < (wheat_kg * 0.85) THEN 1 ELSE 0 END) FROM 'data/allocations.parquet' WHERE fps_code = '{fps}'").fetchone()[0] or 0
            c30 = min((st[0] / tot) * 500, 100); c90 = min((st[1] / tot) * 200, 100); res = 100 - (st[2] or 100); an_s = an * 100; rep = (1 - (st[3] or 1)) * 100
            comp = (c30 * 0.3) + (c90 * 0.15) + (res * 0.2) + (an_s * 0.25) + (rep * 0.1); tier = "low"
            if comp >= 75: tier = "critical"
            elif comp >= 50: tier = "high"
            elif comp >= 25: tier = "medium"
            rec = db.query(FpsRiskScore).filter(FpsRiskScore.fps_code == fps).first()
            if rec: rec.complaints_30d = st[0]; rec.complaints_90d = st[1]; rec.resolution_rate = st[2] or 100; rec.pos_anomaly_score = an_s; rec.composite_risk_score = comp; rec.risk_tier = tier; rec.last_calculated_at = datetime.now(); db.commit()
        finally: db.close()
analytics_service = AnalyticsService()