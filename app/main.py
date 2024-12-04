from fastapi import FastAPI
from app.routers import valuation

app = FastAPI()
app.include_router(valuation.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
