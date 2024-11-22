#!/usr/bin/env python3
"""DB module"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User
from typing import Dict


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """returns a User object and saves it to the database"""
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """find user using given keyword arguments"""
        a = list(User.__dict__.keys())
        attrs = [attr for attr in a if attr[0] != '_']
        s_attrs = (set(attrs))
        s_kwargs = (set(kwargs.keys()))
        if len(s_kwargs.difference(s_attrs)) != 0:
            raise InvalidRequestError
        session = self._session
        user = session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """updates a user"""
        a = list(User.__dict__.keys())
        attrs = [attr for attr in a if attr[0] != '_']
        s_attrs = (set(attrs))
        s_kwargs = (set(kwargs.keys()))
        if len(s_kwargs.difference(s_attrs)) != 0:
            raise ValueError
        user_to_update = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            user_to_update.__setattr__(k, v)
        return None
