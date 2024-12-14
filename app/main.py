from fastapi import FastAPI
from sqlalchemy import create_engine
from app.routers import valuation, oauth, users
from fastapi.middleware.cors import CORSMiddleware
from app.model.users import Base
import os
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

app.include_router(valuation.router, prefix="/user", tags=["valuation"])
app.include_router(users.router, prefix="/user", tags=["registration"])
app.include_router(oauth.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3006"],  # React's development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=create_engine(os.getenv("SQLITE_PATH")))

