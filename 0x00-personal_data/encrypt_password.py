#!/usr/bin/env python3
"""A module to encrypt password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """a function that hashes a password"""
    return bcrypt.hashpw(bytes(password, "UTF-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """a function to validate a password"""
    return bcrypt.hashpw(bytes(password, "UTF-8"), hashed_password)\
        == hashed_password
