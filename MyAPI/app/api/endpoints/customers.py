from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.customer import Customer, SegmentEnum
from app.services import customer_service

router = APIRouter()

@router.get("/", response_model=dict)
async def list_customers(
    full_name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    segment: Optional[SegmentEnum] = Query(None),
    city: Optional[str] = Query(None),
    interest: Optional[str] = Query(None)
):
    """Liste l'annuaire des clients avec filtres complexes."""
    customers = customer_service.get_filtered_customers(full_name, email, segment, city, interest)
    return {"customers": customers}

@router.post("/", response_model=Customer, status_code=201)
async def create_customer(customer: Customer):
    """Créer un nouveau profil client."""
    return customer_service.upsert_customer(customer)

@router.get("/{id}", response_model=Customer)
async def get_customer(id: str):
    """Récupère un profil client par ID."""
    customer = customer_service.get_customer_by_id(id)
    if not customer:
        raise HTTPException(status_code=404, detail="Client introuvable")
    return customer

@router.put("/{id}", response_model=Customer)
async def update_customer(id: str, customer: Customer):
    """Mise à jour complète du profil."""
    if id != customer.customer_id:
        raise HTTPException(status_code=400, detail="L'ID dans l'URL ne correspond pas à l'ID du corps")
    
    existing = customer_service.get_customer_by_id(id)
    if not existing:
        raise HTTPException(status_code=404, detail="Client introuvable")
        
    return customer_service.upsert_customer(customer)