#!/usr/bin/env python3
""" Module session_exp_auth """
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """ Class SessionExpAuth that inherits from SessionAuth """

    def __init__(self):
        """ Overload __init__ method """
        super().__init__()
        self.session_duration = int(os.getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """ Overload create_session method """
        session_id = super().create_session(user_id)
        if session_id is not None:
            session_dict = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
            self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Overload user_id_for_session_id method """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict['user_id']

        if 'created_at' not in session_dict:
            return None

        created_at = session_dict['created_at']
        expiration_time = created_at + timedelta(
            seconds=self.session_duration)

        if expiration_time < datetime.now():
            return None

        return session_dict['user_id']
