from http.client import HTTPException
from databases.fake_db import *
from schemas.items import *
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{item_id}")
def read_item(item_id : str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id" : items[item_id]}

@router.put("/{item_id}/")
def update_item(item_id : str, item : Item):
    items[item_id] = item.model_dump(exclude_unset=True)
    return {"item_id" : items[item_id]}


@router.patch("/{item_id}")
def partial_update_item(item_id: str, item: ItemBase):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    stored_item_data = items[item_id]
    stored_item_model = ItemBase.model_validate(stored_item_data)  # Use Pydantic's model_validate
    update_data = item.model_dump(exclude_unset=True)
    updated_item = stored_item_model.model_copy(update=update_data)

    items[item_id] = updated_item.dict()
    return updated_item
