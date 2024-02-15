#!/usr/bin/env python3
""" new authentication system, based on Session ID stored in database """
from models.base import Base


class UserSession(Base):
    """ Implements a UserSession class """

    def __init__(self, *args: list, **kwargs: dict):
        """ Class initialization method """
        super().__init__(*args, **kwargs)
        self.user_id: str = kwargs.get('user_id')
        self.session_id: str = kwargs.get('session_id')
