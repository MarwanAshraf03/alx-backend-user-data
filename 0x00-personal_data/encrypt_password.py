#!/usr/bin/env python3
"""A module to encrypt password"""
import bcrypt


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(bytes(password, "UTF-8"), bcrypt.gensalt())
