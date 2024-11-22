#!/usr/bin/env python3
"""authentication module"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """a function that hashes a password"""
    return hashpw(bytes(password, "UTF-8"), gensalt())
