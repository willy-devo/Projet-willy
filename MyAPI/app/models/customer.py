from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from enum import Enum

class SegmentEnum(str, Enum):
    VIP = "VIP"
    Standard = "Standard"
    Nouveau = "Nouveau"

class CustomerMetadata(BaseModel):
    account_created: Optional[str] = Field(None, example="2024-01-15")
    preferred_language: Optional[str] = Field(None, example="fr")

class Customer(BaseModel):
    customer_id: str = Field(..., pattern='^CUST-[0-9]{3}$', example="CUST-001")
    full_name: str = Field(..., example="Jean Dupont")
    email: EmailStr = Field(..., example="j.dupont@email.com")
    segment: SegmentEnum = Field(..., example="VIP")
    loyalty_points: int = Field(0, ge=0)
    interests: List[str] = Field(default_factory=list)
    metadata: Optional[CustomerMetadata] = None