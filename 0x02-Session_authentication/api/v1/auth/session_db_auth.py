#!/usr/bin/env python3
""" Module session_db_auth """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Class SessionDBAuth that inherits from SessionExpAuth """

    def create_session(self, user_id=None):
        """ Overload create_session method """
        session_id = super().create_session(user_id)
        if session_id is not None:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Overload user_id_for_session_id method """
        user_id = super().user_id_for_session_id(session_id)
        if user_id is not None:
            user_session = UserSession.search({'session_id': session_id})
            if user_session:
                return user_session[0].user_id
        return None

    def destroy_session(self, request=None):
        """ Overload destroy_session method """
        if super().destroy_session(request):
            session_id = self.session_cookie(request)
            user_sessions = UserSession.search({'session_id': session_id})
            for user_session in user_sessions:
                user_session.remove()
            return True
        return False
