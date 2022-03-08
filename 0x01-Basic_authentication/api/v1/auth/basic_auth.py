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
    pass
