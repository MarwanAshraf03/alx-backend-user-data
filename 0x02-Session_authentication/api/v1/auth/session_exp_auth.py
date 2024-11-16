#!/usr/bin/env python3
"""A module for expiration date session authentication"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime

from models.user import User


class SessionExpAuth(SessionAuth):
    """
    a class that inherits SessionAuth and
    makes sessions with expiary date
    """
    def __init__(self):
        """an overloaded function of the corresponding parent's function"""
        session_duration = getenv("SESSION_DURATION")
        try:
            self.session_duration = int(session_duration)
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """an overloaded function of the corresponding parent's function"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def current_user(self, request=None):
        """that returns a User instance based on a cookie value"""
        s_cookie = self.session_cookie(request)
        id = self.user_id_by_session_id.get(s_cookie)
        return User.get(id["user_id"])

    def user_id_for_session_id(self, session_id=None):
        """an overloaded function of the corresponding parent's function"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id]["user_id"]
        if "created_at" not in self.user_id_by_session_id[session_id].keys():
            return None
        created_at = self.user_id_by_session_id[session_id]["created_at"]
        if created_at.second - self.session_duration < datetime.now().second:
            return None
        return self.user_id_by_session_id[session_id]["user_id"]
