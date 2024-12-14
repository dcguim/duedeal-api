from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi import HTTPException
from passlib.context import CryptContext
import json
import os
from dotenv import load_dotenv
load_dotenv()

def get_sqlite_session():
    # SQLite setup
    engine = create_engine(os.getenv("SQLITE_PATH"))
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    sqlite_session = SessionLocal() 
    try:
        yield sqlite_session  # Provide the session to the endpoint
    finally:
        sqlite_session.close()  # Ensure the session is closed after the request

def load_json(path):
    try:
        with open(path, "r") as fd:
            return json.load(fd)
    except FileNotFoundError:
        raise HTTPException(status_code=500,
                            detail="JSON file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500,
                            detail="Failed to parse JSON file")

# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plain text password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)
