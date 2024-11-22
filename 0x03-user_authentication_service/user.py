#!/usr/bin/env python3
"""A module to create table users"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class User(Base):
    """the mapping declaration of users table"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __init__(self, email, hashed_password):
        """class constructor"""
        self.email = email
        self.hashed_password = hashed_password
