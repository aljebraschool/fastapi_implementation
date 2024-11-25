from typing import Annotated

from fastapi import Depends


def common_parameters(q : str | None = None, skip : int = 0, limit : int = 100):
    return {"q": q, "skip": skip, "limit": limit}

class CommonQueryParameter:
    def __init__(self, q : str | None = None, skip : int = 0, limit : int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

CommonDep = Annotated[CommonQueryParameter, Depends()]
