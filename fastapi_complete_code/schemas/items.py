from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional


class Image(BaseModel):
    name : str
    url : HttpUrl

"""
Request body : used by the client (browser) to send data to  your API. 
It should be declared with a Pydantic class
"""

#define the request body class
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = Field(
        None,
        description="Optional detail of item description",
        title="item description",
    )  # optional
    price: float = Field(ge=50, description="price of an item")  # Corrected
    tags: list[str] = Field(default_factory=list)
    image: Optional[str] = None
    tax: Optional[float] = None  # optional
    timestamp: Optional[str] = None  # Include 'timestamp' as optional


class Item(ItemBase):
    timestamp : datetime