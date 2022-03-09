#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union


def _hash_password(password: str) -> str:
    """Returns input password hashed with bcrypt.hashpw
    """
    binary_password = bytes(password, "ascii")
    return bcrypt.hashpw(binary_password, bcrypt.gensalt())
