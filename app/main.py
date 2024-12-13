from fastapi import FastAPI, Depends
from app.routers import valuation, oauth
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

app.include_router(valuation.router, prefix="/user", tags=["valuation"])

app.include_router(oauth.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3006"],  # React's development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
