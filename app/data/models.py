from datetime import datetime
from sqlalchemy import JSON, Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

class User(Base):
    """
    User class
    """
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    google_id = Column(String, unique=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    full_name = Column(String)
    profile_picture = Column(String)
    role = Column(String, default='user')
    preferences = Column(JSON)  # If using a JSON field to store preferences
    date_joined = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    status = Column(String, default='active')
    bio = Column(String)
    location = Column(String)
    token = relationship('token', back_populates='user')  # Example if tokens is a relationship
    # Other columns...

class Token(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    token = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    expiry_date = Column(DateTime)
    user = relationship('User', back_populates='token')

class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    # Add other columns as needed

class Blacklist(Base):
    
    __tablename__ = 'blacklist'
    id = Column(Integer, primary_key=True)
    token = Column(String, nullable=False)
    
engine = create_engine('sqlite:///data.db')
Base.metadata.create_all(engine)

