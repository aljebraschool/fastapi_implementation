from http.client import HTTPException

from fastapi import APIRouter, FastAPI
from schemas.users import *
from databases.fake_db import *

router = APIRouter(
    prefix = "/users",
    tags = ["users"]
)

def fake_password_hasher(raw_password : str):
    return "supersecret" + raw_password

@router.post("/", response_model=UserOut)
def create_user(user_in : UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    save_user = UserInDB(**user_in.model_dump(), hashed_password = hashed_password)
    return save_user

