#!/usr/bin/env python3
"""authentication module"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
# from typing import Union


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

    def create_session(self, email: str) -> str:
        """creates a session for a user"""
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        user.session_id = session_id
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """gets user using their session id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroys a session"""
        self._db.update_user(user_id=user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """generates a reset password token"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
        except NoResultFound:
            raise ValueError
