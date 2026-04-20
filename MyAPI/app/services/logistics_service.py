from app.storage.json_adapter import load_data
from app.models.logistics import Shipment, ShipmentStep, StockAlert
from typing import List, Optional

def get_shipment_by_id(order_id: str) -> Optional[Shipment]:
    """Récupère l'état d'expédition basé sur une commande."""
    data = load_data("sales") # Utilise orders.json
    orders = data.get("orders", [])
    order = next((o for o in orders if o["order_id"] == order_id), None)
    
    if not order:
        return None
        
    # Simulation de mapping entre le statut simple et les étapes logistiques
    step_map = {"pending": "preparing", "shipped": "in_transit", "delivered": "delivered"}
    
    return Shipment(
        order_id=order_id,
        tracking_number=f"GE-{order_id.split('-')[-1]}-FR",
        current_step=step_map.get(order["status"], "preparing"),
        estimated_delivery="2026-04-18"
    )

def check_low_stock(threshold: int = 5) -> List[StockAlert]:
    """Identifie les produits sous le seuil de sécurité."""
    data = load_data("inventory") # Utilise products.json
    products = data.get("products", [])
    
    alerts = []
    for p in products:
        if p["stock"] < threshold:
            alerts.append(StockAlert(product_id=p["id"], current_stock=p["stock"]))
    return alerts