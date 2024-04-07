from sqlalchemy import create_engine, Column, String, Boolean, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime

from models import User, Message, Base

# Database configuration (moved from main code)
SQLALCHEMY_DATABASE_URL = "sqlite:///./eNtweniChat.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base.metadata.create_all(bind=engine)

def get_session():
    """
    Provides a new SQLAlchemy session object.
    """
    session = SessionLocal()
    yield session
    session.close()

def create_user(phone_number, hashed_password):
    """
    Creates a new user in the database.
    """
    session = next(get_session())
    user = User(phone_number=phone_number, is_registered=True, password=hashed_password)
    session.add(user)
    session.commit()
    session.close()

# Similar functions for user retrieval, message storage, and retrieval (implement based on your needs)

