from app.storage.json_adapter import load_data
from app.models.product import Product, ProductDetail
from typing import List, Optional

def get_all_products(category: Optional[str] = None, brand: Optional[str] = None) -> List[Product]:
    """Liste les produits avec filtres optionnels sur la catégorie et la marque."""
    data = load_data("inventory") # Charge products.json
    products = data.get("products", [])
    
    if category:
        products = [p for p in products if p["category"].lower() == category.lower()]
    if brand:
        products = [p for p in products if p["brand"].lower() == brand.lower()]
    
    return [Product(**p) for p in products]

def get_product_by_id(product_id: str) -> Optional[ProductDetail]:
    """Récupère la fiche technique complète d'un produit."""
    data = load_data("inventory")
    products = data.get("products", [])
    prod_data = next((p for p in products if p["id"] == product_id), None)
    
    return ProductDetail(**prod_data) if prod_data else None

def get_products_by_ids(product_ids: List[str]) -> List[Product]:
    """Utile pour retourner les résultats d'une recherche sémantique externe."""
    data = load_data("inventory")
    products = data.get("products", [])
    results = [p for p in products if p["id"] in product_ids]
    return [Product(**p) for p in results]