from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.product import Product, ProductDetail
from app.services import inventory_service

router = APIRouter()

@router.get("/", response_model=dict)
async def list_products(category: Optional[str] = None, brand: Optional[str] = None):
    """Liste le catalogue de produits avec filtres."""
    products = inventory_service.get_all_products(category, brand)
    return {"products": products}

@router.get("/search", response_model=dict)
async def search_products(q: str = Query(..., description="Requête en langage naturel")):
    """
    Recherche sémantique par intention. 
    Note : En production, cet endpoint appelle l'Agent Discovery via MCP.
    """
    # Ici, l'intégration appellerait la base vectorielle (ChromaDB)
    # Pour l'exemple, nous retournons une liste vide ou simulée
    return {"results": []}

@router.get("/{id}", response_model=ProductDetail)
async def read_product(id: str):
    """Récupère les détails techniques d'un produit."""
    product = inventory_service.get_product_by_id(id)
    if not product:
        raise HTTPException(status_code=404, detail="Le produit spécifié n'existe pas")
    return product