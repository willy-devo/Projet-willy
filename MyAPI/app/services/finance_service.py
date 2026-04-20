from app.storage.json_adapter import load_data
from app.models.finance import Invoice, RevenueStats
from typing import List, Optional

def get_invoice_by_order(order_id: str) -> Optional[Invoice]:
    """Génère une facture à partir des données d'une commande."""
    data = load_data("finance") # Charge orders.json via l'adaptateur
    orders = data.get("orders", [])
    
    order = next((o for o in orders if o["order_id"] == order_id), None)
    if not order:
        return None
    
    # Calcul financier simple (TVA 20%)
    ttc = order["total_amount"]
    ht = round(ttc / 1.2, 2)
    
    return Invoice(
        invoice_id=f"INV-{order_id.split('-')[-1]}",
        order_id=order_id,
        amount_ht=ht,
        amount_ttc=ttc
    )

def get_global_revenue() -> RevenueStats:
    """Calcule le chiffre d'affaires total sur l'ensemble des commandes."""
    data = load_data("finance")
    orders = data.get("orders", [])
    
    total = sum(o["total_amount"] for o in orders)
    return RevenueStats(
        total_revenue=round(total, 2),
        order_count=len(orders)
    )