from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.sales import Order, OrderStatus, CheckoutRequest
from app.services import sales_service

router = APIRouter()

@router.get("/", response_model=dict)
async def list_orders(
    customer_id: Optional[str] = Query(None), 
    status: Optional[OrderStatus] = Query(None)
):
    """Liste l'historique global des transactions."""
    orders = sales_service.get_orders(customer_id, status)
    return {"orders": orders}

@router.get("/{id}", response_model=Order)
async def read_order(id: str):
    """Détails d'une commande spécifique."""
    order = sales_service.get_order_by_id(id)
    if not order:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    return order

@router.post("/checkout", response_model=Order, status_code=201)
async def checkout(request: CheckoutRequest):
    """Création d'une nouvelle commande."""
    # Ici, on pourrait ajouter une validation de stock via inventory_service
    return sales_service.create_new_order(request)