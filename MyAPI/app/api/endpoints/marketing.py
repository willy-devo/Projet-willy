from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models.marketing import LoyaltyProfile, CampaignRequest, MarketTrends
from app.services import marketing_service

router = APIRouter()

@router.get("/loyalty/{cust_id}", response_model=LoyaltyProfile)
async def get_loyalty(cust_id: str):
    """Récupère le solde de points et les avantages fidélité."""
    profile = marketing_service.get_loyalty_status(cust_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Données de fidélité introuvables")
    return profile

@router.post("/campaigns", status_code=202)
async def launch_campaign(campaign: CampaignRequest, background_tasks: BackgroundTasks):
    """Déclenche une campagne marketing basée sur le ciblage sémantique."""
    targets = marketing_service.get_target_audience(campaign.target_interest)
    # Simulation d'envoi d'emails en tâche de fond
    return {"message": f"Campagne acceptée pour {len(targets)} clients."}

@router.get("/trends", response_model=MarketTrends)
async def get_trends():
    """Analyse des tendances (données simulées pour l'exemple)."""
    return MarketTrends(
        top_categories=["Laptops", "GPU"],
        trending_products=[{"product_id": "PROD-101", "view_count": 1250}]
    )