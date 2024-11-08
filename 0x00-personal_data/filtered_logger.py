#!/usr/bin/env python3
"""a filtered logger module"""
import re
from typing import List


def filter_datum(fields: List, redaction: str, message: str, separator: str)\
        -> str:
    """obfuscated message generator"""
    new_message: str = message
    for i in fields:
        new_message: str = re.sub(f"{separator}{i}=(.*?){separator}",
                             f"{separator}{i}={redaction}{separator}",
                             new_message)
    return new_message
