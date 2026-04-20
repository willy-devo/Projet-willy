from app.storage.json_adapter import load_data, save_data
from app.models.sales import Order, OrderStatus, CheckoutRequest
from typing import List, Optional
import uuid
from datetime import datetime

def get_orders(customer_id: Optional[str] = None, status: Optional[OrderStatus] = None) -> List[Order]:
    """Liste l'historique des transactions avec filtres optionnels."""
    data = load_data("sales") # Charge orders.json
    orders = data.get("orders", [])
    
    if customer_id:
        orders = [o for o in orders if o["customer_id"] == customer_id]
    if status:
        orders = [o for o in orders if o["status"] == status]
        
    return [Order(**o) for o in orders]

def get_order_by_id(order_id: str) -> Optional[Order]:
    """Récupère les détails d'une commande spécifique."""
    data = load_data("sales")
    orders = data.get("orders", [])
    order_data = next((o for o in orders if o["order_id"] == order_id), None)
    return Order(**order_data) if order_data else None

def create_new_order(checkout: CheckoutRequest) -> Order:
    """Valide la transaction et enregistre la commande."""
    data = load_data("sales")
    
    # Simulation de calcul de montant total (devrait normalement interroger inventory_service)
    total = 0.0 # À dynamiser selon les prix réels des produits
    
    new_order = Order(
        order_id=f"CMD-2026-{str(uuid.uuid4())[:3].upper()}",
        customer_id=checkout.customer_id,
        items=checkout.items,
        total_amount=total,
        status=OrderStatus.pending,
        payment_method=checkout.payment_method,
        created_at=datetime.now()
    )
    
    data.setdefault("orders", []).append(new_order.dict())
    save_data("sales", data) # Persistance dans orders.json
    return new_order