from fastapi import FastAPI
from app.routers import valuation
from app.model.users import Base

app = FastAPI()
app.include_router(valuation.router)
