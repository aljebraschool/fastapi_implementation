from pydantic import BaseModel
from typing import Optional

class ProductOut(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Optional[list[str]] = []
