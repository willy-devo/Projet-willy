from fastapi import APIRouter, HTTPException
from typing import List
from app.models.logistics import Shipment, StockAlert, SupportTicket
from app.services import logistics_service

router = APIRouter()

@router.get("/shipments/{id}", response_model=Shipment)
async def get_shipment(id: str):
    """Tracking en temps réel de la livraison."""
    shipment = logistics_service.get_shipment_by_id(id)
    if not shipment:
        raise HTTPException(status_code=404, detail="Expédition introuvable")
    return shipment

@router.post("/support/ticket", status_code=201)
async def create_ticket(ticket: SupportTicket):
    """Ouverture d'un incident SAV."""
    # Ici, on pourrait enregistrer dans un fichier tickets.json
    return {"ticket_id": "TICK-8829-X", "status": "open"}

@router.get("/stock/status", response_model=dict)
async def get_alerts():
    """État d'alerte sur les stocks critiques."""
    alerts = logistics_service.check_low_stock()
    return {"alerts": alerts}