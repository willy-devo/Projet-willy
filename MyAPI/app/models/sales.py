from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    pending = "pending"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class OrderItem(BaseModel):
    product_id: str = Field(..., example="PROD-101")
    quantity: int = Field(..., gt=0, example=1)

class Order(BaseModel):
    order_id: str = Field(..., description="Format CMD-YYYY-XXX")
    customer_id: str = Field(..., description="ID Client CUST-XXX")
    items: List[OrderItem]
    total_amount: float
    status: OrderStatus
    payment_method: str
    created_at: datetime = Field(default_factory=datetime.now)

class CheckoutRequest(BaseModel):
    customer_id: str
    items: List[OrderItem]
    payment_method: str