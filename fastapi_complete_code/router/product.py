from schemas.product import *
from fastapi import APIRouter, HTTPException
from databases.fake_db import *

router = APIRouter(
    prefix="/product",
    tags=["product"]
)

@router.get("/", response_model=ProductOut)
def read_users(user_id : str):
    if user_id not in items:
        raise HTTPException(status_code = 404, detail="User not found")
    user_data = items[user_id]
    return user_data
