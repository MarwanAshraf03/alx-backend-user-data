#!/usr/bin/env python3
"""a filtered logger module"""
import os
import re
from typing import List
import logging
import mysql.connector


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

    def __init__(self, fields: List[str]):
        """constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.__fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formatting the record"""
        record.msg = filter_datum(self.__fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super().format(record)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """a function to return logging.Logger object"""
    formatter = RedactingFormatter(list(PII_FIELDS))
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """a function that returns a mysql database connection"""
    PERSONAL_DATA_DB_USERNAME: str = os.getenv("PERSONAL_DATA_DB_USERNAME",
                                               "root")
    PERSONAL_DATA_DB_PASSWORD: str = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    PERSONAL_DATA_DB_HOST: str = os.getenv("PERSONAL_DATA_DB_HOST",
                                           "localhost")
    PERSONAL_DATA_DB_NAME: str = os.getenv("PERSONAL_DATA_DB_NAME")
    conn = mysql.connector.connect(
            user=PERSONAL_DATA_DB_USERNAME,
            password=PERSONAL_DATA_DB_PASSWORD,
            host=PERSONAL_DATA_DB_HOST,
            database=PERSONAL_DATA_DB_NAME,
    )
    return conn


def main():
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        # ';'.join(row)
        print(type(row))
        print(row)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()