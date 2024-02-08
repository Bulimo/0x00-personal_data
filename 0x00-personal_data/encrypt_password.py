#!/usr/bin/env python3
""" Module encrypt_password """

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes and salts the provided password using bcrypt.
    Args:
      password (str): The plain text password to be hashed.

    Returns:
      bytes: The salted and hashed password as a byte string.
    """
    # Generate a salt and hash the password
    # converting password to array of bytes
    bytes = password.encode('utf-8')

    # generating the salt
    salt = bcrypt.gensalt()

    # Hashing the password
    hashed_password = bcrypt.hashpw(bytes, salt)
    # hashed_password = bcrypt.hashpw(password.encode('utf-8'),
    # bcrypt.gensalt())

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates if the provided password.
    Args:
      hashed_password (bytes): The hashed password stored in the database.
      password (str): The plain text password to be validated.

    Returns:
      bool: True if the provided password matches else False.
    """
    # Use bcrypt to check if the password matches the hashed password
    # return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    # encoding user password
    userBytes = password.encode('utf-8')

    # checking password
    result = bcrypt.checkpw(userBytes, hashed_password)

    return result
