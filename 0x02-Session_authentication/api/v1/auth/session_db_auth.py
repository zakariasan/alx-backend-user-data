#!/usr/bin/env python3
""" Module for managing sessions stored in a database. """
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session management class storing sessions in a database."""

    def create_session(self, user_id=None):
        """
        Create a session for a user and store it in the database.
        Args:
            user_id (str): The user ID to create a session for.
        Returns:
            str: The session ID if the session is created, otherwise None.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        UserSession.save_to_file()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve a user ID based on a session ID stored in the database.
        Args:
            session_id (str): The session ID to look up.
        Returns:
            str: The user ID if the session is valid, otherwise None.
        """
        if session_id is None:
            return None

        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return None

        user_session = user_session[0]
        expired_time = user_session.created_at + timedelta(
            seconds=self.session_duration
        )
        if expired_time < datetime.utcnow():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """
        Args:
            request: The Flask request object containing the session cookie.
        Returns:
            booif the session was successfully destroyed, otherwise False.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return False

        user_session = user_session[0]
        try:
            user_session.remove()
            UserSession.save_to_file()
        except Exception:
            return False

        return True
