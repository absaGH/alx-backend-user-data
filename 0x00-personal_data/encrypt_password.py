#!/usr/bin/env python3
"""
Encrypt passwords & test correctens of password provided
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ function that expects one string argument and returns
    a salted, hashed password, which is a byte string"""
    binary_password = bytes(password, "ascii")
    return bcrypt.hashpw(binary_password, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ function that uses bcrypt to validate that the
        provided password matches the hashed password """
    return bcrypt.checkpw(bytes(password, "ascii"), hashed_password)
