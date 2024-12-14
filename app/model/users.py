from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
Base = declarative_base()

class Waitlist(Base):
    __tablename__ = 'waitlist'
    email = Column(String, primary_key=True, nullable=False)

class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    password = Column(String, nullable=False)
