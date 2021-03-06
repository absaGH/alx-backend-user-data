#!/usr/bin/env python3
""" Module of SessionAuth
"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """SesssionAuth class definition
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        sessionID = str(uuid.uuid4())
        self.user_id_by_session_id[sessionID] = user_id
        return sessionID

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance based on a
           cookie value
        """
        sessionID = self.session_cookie(request)
        ID = self.user_id_for_session_id(sessionID)
        user = User.get(ID)

        return user

    def destroy_session(self, request=None):
        """ deletes the user session/logout
        """
        if request is None:
            return False

        sessionID = self.session_cookie(request)

        if not sessionID:
            return False

        if not self.user_id_for_session_id(sessionID):
            return False

        del self.user_id_by_session_id[sessionID]
        return True
