from app.storage.json_adapter import load_data
from app.models.marketing import LoyaltyProfile, LoyaltyTier
from typing import Optional, List

def get_loyalty_status(customer_id: str) -> Optional[LoyaltyProfile]:
    """Calcule le statut de fidélité basé sur les points du client."""
    data = load_data("customers")
    customers = data.get("customers", [])
    cust = next((c for c in customers if c["customer_id"] == customer_id), None)
    
    if not cust:
        return None
        
    points = cust.get("loyalty_points", 0)
    
    # Logique simple de détermination du Tier
    tier = LoyaltyTier.Bronze
    if points >= 2000: tier = LoyaltyTier.Platinum
    elif points >= 1000: tier = LoyaltyTier.Gold
    elif points >= 500: tier = LoyaltyTier.Silver
    
    return LoyaltyProfile(
        customer_id=customer_id,
        points_balance=points,
        tier=tier,
        available_rewards=["Free Shipping"] if points > 100 else []
    )

def get_target_audience(interest: str) -> List[str]:
    """Identifie les emails des clients intéressés par un domaine."""
    data = load_data("customers")
    customers = data.get("customers", [])
    return [c["email"] for c in customers if interest.lower() in [i.lower() for i in c.get("interests", [])]]