# FILE: ration-saathi/backend/app/services/epds.py
from typing import Optional, Dict, Any
from datetime import date
from app.core.config import settings
import json
import os
from app.db.models import RationCard, MonthlyAllocation
from sqlalchemy.orm import Session
from app.db.session import get_db

# Mock data models
class RationCardDetails:
    def __init__(self, card_number: str, state_code: str, district_code: str, 
                 block_code: str, fps_code: str, category: str, 
                 household_head_name: str, total_members: int, 
                 is_active: bool, aadhaar_seeded: bool):
        self.card_number = card_number
        self.state_code = state_code
        self.district_code = district_code
        self.block_code = block_code
        self.fps_code = fps_code
        self.category = category
        self.household_head_name = household_head_name
        self.total_members = total_members
        self.is_active = is_active
        self.aadhaar_seeded = aadhaar_seeded

class AllocationDetails:
    def __init__(self, rice_kg: float, wheat_kg: float, sugar_kg: float, 
                 fps_code: str, month_year: date):
        self.rice_kg = rice_kg
        self.wheat_kg = wheat_kg
        self.sugar_kg = sugar_kg
        self.fps_code = fps_code
        self.month_year = month_year

class BaseEPDSClient:
    def get_ration_card(self, card_number: str) -> Optional[RationCardDetails]:
        raise NotImplementedError
    
    def get_monthly_allocation(self, card_number: str, month_year: date) -> Optional[AllocationDetails]:
        raise NotImplementedError

class MockEPDSClient(BaseEPDSClient):
    def __init__(self):
        # Load mock data from fixtures
        fixtures_path = os.path.join(os.path.dirname(__file__), "../../mock_data/epds_fixtures.json")
        with open(fixtures_path, 'r') as f:
            self.fixtures = json.load(f)
        
        # Create lookup dictionaries for faster access
        self.ration_cards = {
            card["card_number"]: card for card in self.fixtures["ration_cards"]
        }
        
        # Group allocations by card number and month
        self.allocations = {}
        for alloc in self.fixtures["monthly_allocations"]:
            key = (alloc["ration_card_number"], alloc["month_year"])
            self.allocations[key] = alloc

    def get_ration_card(self, card_number: str) -> Optional[RationCardDetails]:
        card_data = self.ration_cards.get(card_number)
        if not card_data:
            return None
            
        return RationCardDetails(
            card_number=card_data["card_number"],
            state_code=card_data["state_code"],
            district_code=card_data["district_code"],
            block_code=card_data["block_code"],
            fps_code=card_data["fps_code"],
            category=card_data["category"],
            household_head_name=card_data["household_head_name"],
            total_members=card_data["total_members"],
            is_active=card_data["is_active"],
            aadhaar_seeded=card_data["aadhaar_seeded"]
        )

    def get_monthly_allocation(self, card_number: str, month_year: date) -> Optional[AllocationDetails]:
        month_str = month_year.strftime("%Y-%m-%d")
        alloc_data = self.allocations.get((card_number, month_str))
        if not alloc_data:
            return None
            
        return AllocationDetails(
            rice_kg=float(alloc_data["rice_kg"]),
            wheat_kg=float(alloc_data["wheat_kg"]),
            sugar_kg=float(alloc_data["sugar_kg"]),
            fps_code=alloc_data["fps_code"],
            month_year=month_year
        )

class RealEPDSClient(BaseEPDSClient):
    """
    Stub for real e-PDS API integration.
    In a real implementation, this would make HTTP requests to state e-PDS APIs.
    """
    def __init__(self):
        self.api_base_url = settings.EPDS_API_BASE_URL
        self.api_key = settings.EPDS_API_KEY
        # In reality, we would set up proper HTTP client with auth headers, etc.

    def get_ration_card(self, card_number: str) -> Optional[RationCardDetails]:
        # Placeholder for real API call
        # In reality: 
        # 1. Make HTTP request to e-PDS API endpoint for ration card details
        # 2. Parse response
        # 3. Return RationCardDetails object
        # For now, return None to indicate not implemented
        return None

    def get_monthly_allocation(self, card_number: str, month_year: date) -> Optional[AllocationDetails]:
        # Placeholder for real API call
        # In reality:
        # 1. Make HTTP request to e-PDS API endpoint for monthly allocation
        # 2. Parse response
        # 3. Return AllocationDetails object
        # For now, return None to indicate not implemented
        return None

def get_epds_client() -> BaseEPDSClient:
    """
    Factory function to get the appropriate EPDS client based on configuration.
    """
    if settings.USE_MOCK_EPDS:
        return MockEPDSClient()
    else:
        return RealEPDSClient()
