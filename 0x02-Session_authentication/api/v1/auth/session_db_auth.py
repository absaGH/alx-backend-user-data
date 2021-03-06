#!/usr/bin/env python3
""" Module to handle expiration date of Session
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """definition of clas SessionDBAuth"""

    def create_session(self, user_id=None):
        """
            create a new Session to Database
        """
        sessionID = super().create_session(user_id)

        if sessionID is None:
            return None

        user_session = UserSession(
            user_id=user_id,
            sessionID=sessionID
        )

        if user_session is None:
            return None

        user_session.save()
        UserSession.save_to_file()

        return sessionID

    def user_id_for_session_id(self, session_id=None):
        """
            create user id to session
        """
        if session_id is None:
            return None

        UserSession.load_from_file()
        userSession = UserSession.search({'session_id': session_id})

        if not userSession:
            return None

        user = userSession[0]

        if user is None:
            return None

        expire_time = user.created_at + \
            timedelta(seconds=self.session_duration)

        if expire_time < datetime.now():
            return None

        return user.user_id

    def destroy_session(self, request=None):
        """ delete the auth session if this
        """
        if request is None:
            return False

        sessionID = self.session_cookie(request)

        if sessionID is None:
            return False

        user_id = self.user_id_for_session_id(sessionID)
        if not user_id:
            return False

        user_session = UserSession.search({'session_id': session_id})
        if not user_session or user_session is None:
            return False

        try:
            user_session[0].remove()
            UserSession.save_to_file()
        except Exception:
            return False

        return True
