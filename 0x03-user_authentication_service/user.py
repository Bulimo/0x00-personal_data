#!/usr/bin/env python3
"""
Module user
Creates SQLAlchemy model named User for a database table
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column

Base = declarative_base()


class User(Base):
    """ User maodel class """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(length=250), nullable=False)
    hashed_password = Column(String(length=250), nullable=False)
    session_id = Column(String(length=250), nullable=True)
    reset_token = Column(String(length=250), nullable=True)
