#!/usr/bin/env python3
"""template module for all authentication system"""
from typing import List, TypeVar
from flask import request


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns flase"""
        return False

    def authorization_header(self, request=None) -> str:
        """returns the authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns the current user"""
        return None
