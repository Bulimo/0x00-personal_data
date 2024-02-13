#!/usr/bin/env python3
"""
Module auth
Implements the class Auth for authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Class that defines basic authentication
    Methods:
      - require_auth()
      - authorization_header()
      - current_user()
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method that defines paths
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        # Make sure all paths in excluded_paths end with a '/'
        excluded_paths = [
            p if p.endswith('*') else p + '/' for p in excluded_paths
        ]

        # Check if path matches any excluded paths
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path.rstrip('*')) or \
                    path in excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Method that defines authorization header
        Args:
          - request - the Flask request object
        Returns:
          None
        """
        if request is None:
            return None
        authorization = request.headers.get('Authorization', None)
        return authorization

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """
        Method that returns a User object
        Args:
          - request: the Flask request object
        Returns:
          - User object
        """
        return None
