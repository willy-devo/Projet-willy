from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class LoyaltyTier(str, Enum):
    Bronze = "Bronze"
    Silver = "Silver"
    Gold = "Gold"
    Platinum = "Platinum"

class LoyaltyProfile(BaseModel):
    customer_id: str
    points_balance: int
    tier: LoyaltyTier
    available_rewards: List[str] = []

class CampaignRequest(BaseModel):
    campaign_name: str
    target_interest: str
    discount_rate: int = Field(..., ge=5, le=50)

class MarketTrends(BaseModel):
    top_categories: List[str]
    trending_products: List[dict]