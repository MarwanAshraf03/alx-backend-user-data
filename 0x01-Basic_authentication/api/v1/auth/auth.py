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
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns the authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns the current user"""
        return None
