# FILE: ration-saathi/backend/app/services/entitlement.py
from typing import Optional, Tuple
from datetime import date
import logging
from app.db.models import RationCard, MonthlyAllocation
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.encryption import decrypt
from app.services.epds import get_epds_client, RationCardDetails, AllocationDetails

logger = logging.getLogger(__name__)

async def get_entitlement_voice_script(card_number: str, language: str = 'hi', month_year: date = None) -> str:
    """
    Generate voice script for entitlement announcement.
    Returns formatted prompt template with actual data.
    """
    if month_year is None:
        # Default to current month
        today = date.today()
        month_year = date(today.year, today.month, 1)  # First day of current month
    
    # Try to get data from database first
    db = next(get_db())
    try:
        # Look up ration card by card number
        ration_card = db.query(RationCard).filter(RationCard.card_number == card_number).first()
        
        if not ration_card:
            logger.warning(f"Ration card {card_number} not found in database")
            # Try mock e-PDS as fallback
            epds_client = get_epds_client()
            ration_card_details = epds_client.get_ration_card(card_number)
            if not ration_card_details:
                # Card not found anywhere
                if language == 'hi':
                    return "Yeh card number hamare system mein nahi mila. CSC kendra par jaayein ya 0 dabayein sahayak ke liye."
                else:
                    return "This ration card number was not found in our system. Please visit a CSC center or press 0 for assistance."
            
            # Get allocation from mock e-PDS
            allocation_details = epds_client.get_monthly_allocation(card_number, month_year)
            if not allocation_details:
                # No allocation data
                if language == 'hi':
                    return f"Ration card {card_number} ke liye {month_year.strftime('%B %Y')} ka koi anchalan data nahi mila."
                else:
                    return f"No allocation data found for ration card {card_number} for {month_year.strftime('%B %Y')}."
            
            # We have details from mock e-PDS, but we need the head name
            # Since it's encrypted in mock data, we'll use a placeholder
            head_name = "Patidar"  # Placeholder - in reality would decrypt
            
            # Format month name
            month_name = month_year.strftime("%B %Y")
            
            if language == 'hi':
                return f"Namaste {head_name} ji. Is mahine {month_name} mein, aapko {allocation_details.wheat_kg} kilo gehu aur {allocation_details.rice_kg} kilo chawal milna chahiye. Kya aapko poora anaaj mila? Haan ke liye 1, kam mila toh 2 dabayein."
            else:
                return f"Namaste {head_name} ji. In {month_name}, you should receive {allocation_details.wheat_kg} kg wheat and {allocation_details.rice_kg} kg rice. Did you get the full allocation? Press 1 for yes, 2 for less."
        
        # Card found in database
        # Decrypt the head name
        try:
            head_name = decrypt(ration_card.household_head_name) if ration_card.household_head_name else "Patidar"
        except Exception as e:
            logger.error(f"Failed to decrypt head name for card {card_number}: {str(e)}")
            head_name = "Patidar"  # Fallback
        
        # Look up monthly allocation
        allocation = db.query(MonthlyAllocation).filter(
            MonthlyAllocation.ration_card_id == ration_card.id,
            MonthlyAllocation.month_year == month_year
        ).first()
        
        if not allocation:
            logger.warning(f"No allocation found for card {card_number} for {month_year}")
            # Try to get from e-PDS service
            epds_client = get_epds_client()
            allocation_details = epds_client.get_monthly_allocation(card_number, month_year)
            
            if not allocation_details:
                # No allocation data anywhere
                if language == 'hi':
                    return f"Namaste {head_name} ji. Is mahine {month_year.strftime('%B %Y')} ka koi anchalan data nahi mila."
                else:
                    return f"Namaste {head_name} ji. No allocation data found for {month_year.strftime('%B %Y')}."
            
            # Use allocation details from e-PDS
            wheat_kg = allocation_details.wheat_kg
            rice_kg = allocation_details.rice_kg
        else:
            # Use allocation from database
            wheat_kg = float(allocation.wheat_kg) if allocation.wheat_kg else 0
            rice_kg = float(allocation.rice_kg) if allocation.rice_kg else 0
        
        # Format month name
        month_name = month_year.strftime("%B %Y")
        
        if language == 'hi':
            return f"Namaste {head_name} ji. Is mahine {month_name} mein, aapko {wheat_kg} kilo gehu aur {rice_kg} kilo chawal milna chahiye. Kya aapko poora anaaj mila? Haan ke liye 1, kam mila toh 2 dabayein."
        else:
            return f"Namaste {head_name} ji. In {month_name}, you should receive {wheat_kg} kg wheat and {rice_kg} kg rice. Did you get the full allocation? Press 1 for yes, 2 for less."
            
    except Exception as e:
        logger.error(f"Error generating entitlement voice script for card {card_number}: {str(e)}")
        # Return error message
        if language == 'hi':
            return "Maaf kijiye, kuch teknikal dikkat hai. Kripya phir se try karein ya CSC sahayak se baat karein."
        else:
            return "Sorry, there's a technical issue. Please try again or contact CSC assistant."
    finally:
        db.close()

# Unit tests would go in a separate test file, but here are the test scenarios as comments:
"""
Test scenarios for get_entitlement_voice_script:

1. Card found in DB with allocation:
   - Input: card_number="RJ-BA-2025-00001", language='hi', month_year=2025-10-01
   - Expected: Personalized message with head name, wheat and rice quantities

2. Card not found in DB but found in mock e-PDS:
   - Input: card_number="NONEXISTENT", language='hi', month_year=2025-10-01
   - Expected: Message indicating card not found in system

3. Card found in DB but no allocation:
   - Input: card_number with DB entry but no monthly_allocations for month
   - Expected: Message indicating no allocation data

4. Card not found anywhere:
   - Input: card_number="INVALID", language='hi', month_year=2025-10-01
   - Expected: Message to visit CSC center or press 0 for assistance

5. Language selection - English:
   - Input: card_number="RJ-BA-2025-00001", language='en', month_year=2025-10-01
   - Expected: Same information in English

6. Technical error (DB connection failure):
   - Input: any valid card_number
   - Expected: Technical error message in appropriate language
"""
