import json
import os
from datetime import date
from typing import Optional
from pydantic import BaseModel


class RationCardDetails(BaseModel):
    card_number: str
    head_name: str
    total_members: int
    category: str
    fps_code: str
    is_active: bool


class AllocationDetails(BaseModel):
    card_number: str
    month_year: date
    rice_kg: float
    wheat_kg: float
    sugar_kg: float


class MockEPDSClient:
    def __init__(self):
        try:
            with open(os.path.join("mock_data", "epds_fixtures.json"), "r") as f:
                self.data = json.load(f)
        except Exception:
            self.data = {"cards": [], "allocations": []}

    def get_ration_card(self, num: str) -> Optional[RationCardDetails]:
        card = next((c for c in self.data["cards"] if c["card_number"] == num), None)
        return RationCardDetails(**card) if card else None

    def get_monthly_allocation(self, num: str, dt: date) -> Optional[AllocationDetails]:
        alloc = self.data["allocations"].get(f"{num}_{dt.strftime('%Y-%m')}")
        return AllocationDetails(**alloc) if alloc else None


def get_epds_client():
    from app.core.config import settings
    return MockEPDSClient() if settings.USE_MOCK_EPDS else MockEPDSClient()


epds_client = get_epds_client()
