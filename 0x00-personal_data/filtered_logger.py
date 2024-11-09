#!/usr/bin/env python3
"""a filtered logger module"""
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """obfuscated message generator"""
    new_fields: List[str] = [f"(?<={x}=)[^{separator}]*" for x in fields]
    return re.sub("|".join(new_fields), redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"
    PII_FIELDS = ("email", "phone", "ssn", "password", "ip")

    def __init__(self, fields: List[str]):
        """constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.__fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formatting the record"""
        record.msg = filter_datum(self.__fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """a function to return logging.Logger object"""
    logging.StreamHandler(RedactingFormatter)
    return logging.Logger("user_data", logging.INFO)
