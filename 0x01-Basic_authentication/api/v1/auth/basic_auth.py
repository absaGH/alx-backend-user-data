#!/usr/bin/env python3
"""Basic Auth Class module"""
from api.v1.auth.auth import Auth
from base64 import b64decode, b64encode
import hashlib
from models.base import DATA
from models.user import User
from typing import Tuple, TypeVar


class BasicAuth(Auth):
    """Basic Auth class defintion based on Auth
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization
           header for a Basic Authentication
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if authorization_header[0:6] != 'Basic ':
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Returns the decoded value of Base64 string
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            base64_authorization_header = b64decode(
                base64_authorization_header)
        except Exception:
            return None

        return base64_authorization_header.decode('utf-8')

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Retruns the user email and password
           from Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        auth_header = decoded_base64_authorization_header.split(':', 1)
        return (auth_header[0], auth_header[1])

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Returns the User instance based on his email
           and password
        """
        if user_email is None or type(user_email) is not str:
            return None

        if user_pwd is None or type(user_pwd) is not str:
            return None

        if DATA.get('User') is None:
            return None

        user_list = User.search({'email': user_email})
        if user_list is None:
            return None

        for user in user_list:
            if user.email == user_email and user.is_valid_password(user_pwd):
                return user

        return None
