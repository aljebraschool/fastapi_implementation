from typing import Annotated

from fastapi import HTTPException, Header


def verify_token(x_token : Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code = 400, detail = "X-Token header invalid")

def verify_key(x_key : Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code = 400, detail = "X-Key header invalid")
    return x_key