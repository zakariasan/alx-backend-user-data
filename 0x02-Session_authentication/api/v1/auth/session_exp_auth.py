#!/usr/bin/env python3
""" Module for managing session authentication with expiration. """
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from models.user import User
from os import getenv


class SessionExpAuth(SessionAuth):
    """Session expiration authentication class."""

    def __init__(self):
        """Constructor method."""
        # Get session duration from environment variable
        SESSION_DURATION = getenv('SESSION_DURATION')

        try:
            # Convert session duration to an integer
            session_duration = int(SESSION_DURATION)
        except Exception:
            # Set session duration to 0 if conversion fails
            session_duration = 0

        # Set the session duration
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """
        Create a session with expiration for the given user ID.
        Args:
            user_id (str): The ID of the user for whom to create the session.
        Returns:
            str: The ID of the created session.
        """
        # Create session using superclass method
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        # Store session information with creation timestamp
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        # Store session information in memory
        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the user ID associated with the given session ID.
        Args
            session_id (str): The ID of the session tothe user ID for.
        Returns
            str: The ID of the user associated with the sehas expired.
        """
        if session_id is None:
            return None

        # Check if session ID exists in the session dictionary
        if session_id not in self.user_id_by_session_id.keys():
            return None

        # Retrieve session information
        session_dictionary = self.user_id_by_session_id.get(session_id)

        if session_dictionary is None:
            return None

        # Check session expiration
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')

        created_at = session_dictionary.get('created_at')

        if created_at is None:
            return None

        # Calculate expiration time
        expired_time = created_at + timedelta(seconds=self.session_duration)

        if expired_time < datetime.now():
            return None

        # Return user ID associated with the session
        return session_dictionary.get('user_id')
