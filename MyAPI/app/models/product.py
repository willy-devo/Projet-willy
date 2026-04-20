from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class Product(BaseModel):
    id: str = Field(..., description="Identifiant unique PROD-XXX")
    name: str
    brand: str
    category: str
    price: float

class ProductDetail(Product):
    specs: Dict[str, Any] = Field(default_factory=dict, description="Caractéristiques techniques")
    description: str = Field(..., description="Description riche pour l'analyse sémantique")
    stock: int = Field(..., ge=0)