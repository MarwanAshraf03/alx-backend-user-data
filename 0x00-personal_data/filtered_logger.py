#!/usr/bin/env python3
"""a filtered logger module"""
import re
from typing import List


def filter_datum(fields: List, redaction: str, message: str, separator: str)\
        -> str:
    """obfuscated message generator"""
    new_fields = [f"(?<={x}=)[^;]*" for x in fields]
    return re.sub("|".join(new_fields), redaction, message)
