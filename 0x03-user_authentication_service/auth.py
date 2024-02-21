#!/usr/bin/env python3
""" Module auth """
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Method that takes in a password string arguments and returns bytes.
    The returned bytes is a salted hash of the input password, hashed
    with bcrypt.hashpw
    """
    # Generate a salt and hash the password
    # converting password to array of bytes
    bytes = password.encode('utf-8')

    # generating the salt
    salt = bcrypt.gensalt()

    # Hashing the password
    hashed_password = bcrypt.hashpw(bytes, salt)

    return hashed_password


def _generate_uuid() -> str:
    """ Returns a string representation of a new UUID """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ Initialize class object """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Takes mandatory email and password string arguments and returns
        a User object
        If a user already exist with the passed email, raise a ValueError
        If not, hash the password, save the user to the database using and
        return the User object.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(
                    "User {} already exists.".format(email))
        except NoResultFound:
            pass
        hash_password = _hash_password(password)
        user = self._db.add_user(email=email, hashed_password=hash_password)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Credentials validation
        Search the user by email. If exists, check the password.
        If it matches return True. In any other case, return False
        """
        try:
            user = self._db.find_user_by(email=email)
            pass_bytes = password.encode('utf-8')
            return bcrypt.checkpw(pass_bytes, user.hashed_password)
        except NoResultFound:
            return False
        # return False

    def create_session(self, email: str) -> str:
        """
        Method to generate session ID
        takes an email string argument
        returns the session ID as a string.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            # print(f'user session = {user.session_id}')
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Takes a session_id argument and returns the User or None """
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                # print('No user found in DB')
                pass
        return None

    def destroy_session(self, user_id: id) -> None:
        """
        Destroy session
        Updates the corresponding user's session ID to None
        """
        if user_id:
            self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ Generate reset password token """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return user.reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Hash the password and update the user's hashed_password field
        with the new hashed password and then reset_token field to None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            new_passwd = _hash_password(password)
            self._db.update_user(
                user.id, hashed_password=new_passwd, reset_token=None
            )
        except NoResultFound:
            raise ValueError
