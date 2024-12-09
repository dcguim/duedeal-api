from fastapi import FastAPI
from app.routers import valuation
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(valuation.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3006"],  # React's development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
