#!/usr/bin/env python3
"""template module for all authentication system"""
from typing import List, TypeVar
from flask import request


class Auth:
    """ the template for the authentication system"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns flase"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != "/":
            path = path + "/"
        for i in excluded_paths:
            if i.replace("*", "") in path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns the authorization header"""
        if request is None:
            return None
        if "Authorization" not in request.headers.keys():
            return None
        else:
            return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """returns the current user"""
        return None
