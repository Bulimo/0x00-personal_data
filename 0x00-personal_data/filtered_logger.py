#!/usr/bin/env python3
"""
Module filtered_logger
Implements a simple logger
"""
import re
from typing import List
import logging
import os
import mysql.connector

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initializaing the Redacting Formatter class
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Adds redaction to the specified fields
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Returns the log message obfuscated
    Args:
      fields(list): representing all fields to obfuscate
      redaction(str): representing by what the field will be obfuscated
      message(str): representing the log line
      separator(str): representing character separating fields in message
    """
    for field in fields:
        message = re.sub(r"{}=(.*?){}".format(field, separator),
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """
    function that takes no arguments and returns a logging.Logger object
    """
    # create logger
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    # create console handler and set level to info
    ch = logging.StreamHandler()
    ch_format = RedactingFormatter(list(PII_FIELDS))
    ch.setFormatter(ch_format)
    ch.setLevel(logging.INFO)

    # add ch to logger
    logger.addHandler(ch)

    # set propagate to False
    logger.propagate = False

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ function that returns a connector to the database """
    host: str = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
    database: str = os.environ.get('PERSONAL_DATA_DB_NAME', 'root'),
    user: str = os.environ.get('PERSONAL_DATA_DB_USERNAME'),
    password: str = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    return mysql.connector.connect(host, database, user, password)


def main():
    """
    Function to retrieve all rows in the users table and
    display each row under a filtered format
    """
    db_connection = get_db()
    # Create a cursor
    cursor = db_connection.cursor()

    # Execute a query to retrieve all rows from the users table
    cursor.execute("SELECT * FROM users")

    # Fetch all rows
    rows = cursor.fetchall()
    logger = get_logger()

    for row in rows:
        logger.info(
            "name=%s; email=%s; phone=%s; ssn=%s; password=%s; ip=%s; \
              last_login=%s; user_agent=%s", row[0], row[1], row[2],
            row[3], row[4], row[5], row[6], row[7])


if __name__ == "__main__":
    main()
