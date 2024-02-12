#!/usr/bin/env python3
"""
Module basic_auth
Implements class BasicAuth that inherits from Auth class
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    Implementation of basic authentication
    Methods:
      - extract_base64_authorization_header()
      - decode_base64_authorization_header()
      - extract_user_credentials()
      - user_object_from_credentials()
      - current_user()
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Method to extract base64 from authorization header """
        if authorization_header is None or \
                not isinstance(authorization_header, str):
            return None
        authorization_header = authorization_header.strip()
        base64_val = authorization_header.split(' ')
        if base64_val[0] != 'Basic':
            return None
        return base64_val[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Method returns the decoded value of a Base64 string"""
        if base64_authorization_header is None or \
                not isinstance(base64_authorization_header, str):
            return None
        try:
            base64_bytes = base64_authorization_header.encode('utf-8')
            pword_bytes = base64.b64decode(base64_bytes)
            return pword_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None or \
                not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        # decoded_base64_authorization_header = \
        #     decoded_base64_authorization_header.split(':')
        # return (
        #     decoded_base64_authorization_header[0],
        #     decoded_base64_authorization_header[1]
        # )
        colon_index = decoded_base64_authorization_header.find(':')
        if colon_index == -1 or colon_index == 0:
            return (None, None)
        user = decoded_base64_authorization_header[:colon_index]
        password = decoded_base64_authorization_header[colon_index + 1:]
        return (user, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ returns the User instance based on his email and password """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            user = User.search({'email': user_email})
        except Exception:
            return None
        if len(user) == 0:
            return None
        if user[0].is_valid_password(user_pwd) is False:
            return None
        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """ retrieves the User instance for a request """
        header = self.authorization_header(request)
        authorization = self.extract_base64_authorization_header(header)
        decode = self.decode_base64_authorization_header(authorization)
        credential = self.extract_user_credentials(decode)
        return self.user_object_from_credentials(credential[0], credential[1])
