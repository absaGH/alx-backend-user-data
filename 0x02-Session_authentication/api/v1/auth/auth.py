#!/usr/bin/env python3
"""This class is the template used for authentication
   system that will be implemented
"""
from flask import request
from os import getenv
from typing import List, TypeVar


class Auth():
    """The definition of the class used for
       the authenication system
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """It checks on the file path and authorization
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        if path[-1] != '/':
            path = path + '/'

        for expth in excluded_paths:
            if expth[-1] == '*':
                expth = expth[0:-1]

            if expth in path:
                return False

        if path not in excluded_paths:
            return True

        return False

    def authorization_header(self, request=None) -> str:
        """authorization function used
        """
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user
        """
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request
        """
        if request is None:
            return None

        session_env = getenv('SESSION_NAME', None)
        return request.cookies.get(session_env, None)
