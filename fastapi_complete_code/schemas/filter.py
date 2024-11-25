from pydantic import BaseModel, Field
from typing import List, Literal

class FilterParams(BaseModel):
    """
    Generic filtering and pagination parameters for item listings

    Attributes:
        limit: Maximum number of items to return (1-100)
        offset: Number of items to skip for pagination
        order_by: Field to sort results by
        tags: Optional list of tags to filter items
    """
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: List[str] = Field(default_factory=list)