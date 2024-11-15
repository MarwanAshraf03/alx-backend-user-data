#!/usr/bin/env python3
"""A session authenticator module that inherits from AUTH class"""
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """Session Authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session"""
        if user_id is None:
            return None
        if type(user_id).__name__ != "str":
            return None
        idd = str(uuid4())
        self.user_id_by_session_id[idd] = user_id
        return idd

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        if type(session_id).__name__ != "str":
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """that returns a User instance based on a cookie value"""
        s_cookie = self.session_cookie(request)
        id = self.user_id_by_session_id.get(s_cookie)
        return User.get(id)
