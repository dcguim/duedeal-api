from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer
Base = declarative_base()

class Waitlist(Base):
    __tablename__ = 'waitlist'
    email = Column(String, primary_key=True, nullable=False)
