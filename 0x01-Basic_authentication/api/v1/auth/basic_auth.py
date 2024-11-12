#!/usr/bin/env python3
"""template module for all authentication system"""
from base64 import decode, b64decode, b64encode
from typing import Tuple, TypeVar, Union
from api.v1.auth.auth import Auth
from models.base import Base
from models.user import User


class BasicAuth(Auth):
    """interits from Auth"""
    def extract_base64_authorization_header(self, authorization_header: str)\
            -> str:
        """extracts the header without the `Basic ` word`"""
        if authorization_header is None:
            return None
        if type(authorization_header).__name__ != "str":
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.replace("Basic ", "")

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """decodes authorization header in base64"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header).__name__ != "str":
            return None
        try:
            b64encode(b64decode(base64_authorization_header))\
                == base64_authorization_header
        except Exception:
            return None
        return bytes.decode(b64decode(base64_authorization_header), "utf-8")

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> Tuple[str, str]:
        """returns the user's name and password"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header).__name__ != "str":
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        creds = decoded_base64_authorization_header.split(":")
        return (creds[0], creds[1])

    def user_object_from_credentials(self, user_email: str, user_pwd: str) ->\
            TypeVar('User'):
        """a function that returns a user object"""
        if user_email is None or type(user_email).__name__ != "str":
            return None
        if user_pwd is None or type(user_pwd).__name__ != "str":
            return None
        user_list = User.search({"email": user_email})
        # print(user_list)
        user = None
        for i in user_list:
            if user_email in i.__dict__.values():
                user = i
        if user is None:
            return None
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """gets current user from the request"""
        header = super().authorization_header(request)
        extracted = self.extract_base64_authorization_header(header)
        decoded = self.decode_base64_authorization_header(extracted)
        creds = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(creds[0], creds[1])
