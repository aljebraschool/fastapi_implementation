from typing import Annotated

from fastapi import APIRouter, Query
from schemas.filter import *

router = APIRouter(
    prefix="/filters",
    tags=["filters"],

)

@router.get("/", response_model=FilterParams)
def get_filter_params(filters : Annotated[FilterParams, Query()]):
    return filters