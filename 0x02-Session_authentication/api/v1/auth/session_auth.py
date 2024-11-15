#!/usr/bin/env python3
"""A session authenticator module that inherits from AUTH class"""
from api.v1.auth.auth import Auth
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
