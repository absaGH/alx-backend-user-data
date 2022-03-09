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


def _generate_uuid() -> str:
    """ return a string representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ check if user exists, register and return a User object.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user
        else:
            raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """ locate user by email & check pswd with bcrypt.checkpw.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(bytes(password, "ascii"),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ Find user, generate new UUID, save it in db and session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            sess_id = _generate_uuid()
            self._db.update_user((user.id), session_id=sess_id)

            return sess_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ It takes a session_id & returns the corresponding user.
        """
        if session_id is None:
            return None

        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ takes a user_id & user's session ID to None.
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ generate UUID & update user’s reset_token db
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """ use reset_token to find user & update password user
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id,
                                 reset_token=None,
                                 hashed_password=hashed_password)
        except NoResultFound:
            raise ValueError()
