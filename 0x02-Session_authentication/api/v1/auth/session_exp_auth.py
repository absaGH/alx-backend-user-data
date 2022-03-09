#!/usr/bin/env python3
"""
SessionExpAuth module to handle session expiration date
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from models.user import User
import uuid
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ definition of SessionExpAuth class
    """

    user_id_by_session_id = {}

    def __init__(self):
        """ overloaded init
        """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create a new session
        """
        sessionID = super(SessionExpAuth, self).create_session(user_id)

        if not sessionID:
            return None

        self.user_id_by_session_id[sessionID] = {'user_id': user_id,
                                                 'created_at': datetime.now()}
        return sessionID

    def user_id_for_session_id(self, session_id=None):
        """ Return a User ID based on a Session ID
        """
        if session_id is None:
            return None

        session = self.user_id_by_session_id.get(session_id)

        if session is None:
            return None

        if self.session_duration <= 0:
            return session.get('user_id')

        created_at_session = session.get('created_at')

        if created_at_session is None:
            return None

        duration_session = created_at_session + timedelta(
            seconds=self.session_duration
        )

        if duration_session < datetime.now():
            return None
        return session.get('user_id')
