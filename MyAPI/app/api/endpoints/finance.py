from fastapi import APIRouter, HTTPException
from app.models.finance import Invoice, RevenueStats
from app.services import finance_service

router = APIRouter()

@router.get("/invoices/{order_id}", response_model=Invoice)
async def get_invoice(order_id: str):
    """Récupère la facture liée à une commande spécifique."""
    invoice = finance_service.get_invoice_by_order(order_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Commande ou facture introuvable")
    return invoice

@router.get("/revenue/stats", response_model=RevenueStats)
async def get_revenue_summary():
    """Affiche un résumé global du chiffre d'affaires."""
    return finance_service.get_global_revenue()