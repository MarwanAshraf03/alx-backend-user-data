#!/usr/bin/env python3
"""a filtered logger module"""
import re
from typing import List


def filter_datum(fields: List, redaction: str, message: str, separator: str)\
        -> str:
    """obfuscated message generator"""
    for i in fields:
        message: str = re.sub(f"{separator}{i}=(.*?){separator}",
                             f"{separator}{i}={redaction}{separator}",
                             message)
    return message
