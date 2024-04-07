from sqlalchemy import create_engine, Column, String, Boolean, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime

# Base class for models (moved from main code)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    phone_number: str = Column(String, primary_key=True, index=True)
    is_registered: bool = Column(Boolean, default=False)

class Message(Base):
    __tablename__ = "messages"
    
    id: int = Column(Integer, primary_key=True, index=True)
    sender: str = Column(String)
    receiver: str = Column(String)
    content: str = Column(String)
    read: bool = Column(Boolean, default=False)
    timestamp: datetime = Column(DateTime, default=datetime.utcnow)
