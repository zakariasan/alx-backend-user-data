#!/usr/bin/env python3
"""
Main file
"""
import re
from typing import List
import logging
from os import environ
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str],
        redaction: str, message: str, separator: str) -> str:
    """ filter datum """
    pattern = f"({'|'.join(fields)})=.*?({separator}|$)"
    return re.sub(
        pattern, lambda m: f"{m.group(1)}={redaction}{m.group(2)}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ init """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format """
        msg = super().format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ get logger """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    str_hand = logging.StreamHandler()
    str_hand.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(str_hand)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ get db """
    usr = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    passw = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    cn = mysql.connector.connection.MySQLConnection(user=usr,
                                                    password=passw,
                                                    host=host,
                                                    database=db_name)
    return cn


def main():
    """ main """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    names = [i[0] for i in cursor.description]

    logger = get_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, names))
        logger.info(str_row.strip())

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
