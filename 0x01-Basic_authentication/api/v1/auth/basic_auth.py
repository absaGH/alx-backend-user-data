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
