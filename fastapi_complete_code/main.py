from fastapi import FastAPI, Depends
from router import files, items, users, filters, product


from dependencies.auth import verify_key, verify_token

app = FastAPI(
    title="FastAPI CODE IMPLEMENTATION",
    description="This is the complete code implementation of FastAPI fundamentals",
    # dependencies=[Depends(verify_key), Depends(verify_token)]
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(items.router)
app.include_router(users.router)
app.include_router(files.router)
app.include_router(filters.router)

app.include_router(product.router)






