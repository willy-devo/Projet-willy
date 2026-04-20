from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ShipmentStep(str, Enum):
    preparing = "preparing"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"

class Shipment(BaseModel):
    order_id: str
    carrier: str = "GlobalExpress"
    tracking_number: str
    current_step: ShipmentStep
    estimated_delivery: str

class SupportTicket(BaseModel):
    customer_id: str
    order_id: str
    issue_type: str
    description: str

class StockAlert(BaseModel):
    product_id: str
    current_stock: int
    status: str = "critical"