from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OrderCreate(BaseModel):
    item_name: str
    quantity: int
    total_price: float

class Order(OrderCreate):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
