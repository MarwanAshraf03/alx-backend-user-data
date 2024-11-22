#!/usr/bin/env python3
"""authentication module"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """a function that hashes a password"""
    return hashpw(bytes(password, "UTF-8"), gensalt())


def _generate_uuid() -> str:
    """returns a string representation of a new UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers user to database"""
        user = None
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
        if user is None:
            raise ValueError(f"User {email} already exists")
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """checks if user is valid or not"""
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(bytes(password, "utf-8"), user.hashed_password)
        except NoResultFound:
            return False
