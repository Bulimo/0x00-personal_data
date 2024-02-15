#!/usr/bin/env python3
""" Module session_auth for session aunthentication """
from api.v1.auth.auth import Auth
from models.user import User
from typing import Dict
from uuid import uuid4


class SessionAuth(Auth):
    """ class SessionAuth base for session aunthentication """
    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """ Method that creates a Session ID for a user_id """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Method that returns a User ID based on a Session ID """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """(overload) that returns a User instance based on a cookie value"""
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ method that deletes the user session / logout """
        if request is None:
            return False
        if self.session_cookie(request) is None:
            return False
        session_id = self.session_cookie(request)
        if self.user_id_for_session_id(session_id) is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
