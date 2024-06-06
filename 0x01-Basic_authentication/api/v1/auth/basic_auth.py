#!/usr/bin/env python3
"""
Route module for the API
"""

from api.v1.auth.auth.py import Auth

import re
import base64
import binascii
from typing import Tuple, TypeVar, Optional

from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic authentication class implementing the Basic Auth mechanism."""

    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> Optional[str]:
        """
        Extracts the Base64 part of the Authheader for Basic Authentication.

        Args:
            authorization_header (str): The header from the request.

        Returns:
            Optional[str]: The Base64 encodeor None if the header is invalid.
        """
        if isinstance(authorization_header, str):
            pattern = r'Basic (?P<token>.+)'
            match = re.fullmatch(pattern, authorization_header.strip())
            if match:
                return match.group('token')
        return None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> Optional[str]:
        """
        Decodes a Base64 encoded authorization header.

        Args:
            base64_authorization_header (str): The Base64 encoded credentials.

        Returns:
            Optional[str]: The decoded crea string, or None if decoding fails.
        """
        if isinstance(base64_authorization_header, str):
            try:
                decoded_bytes = base64.b64decode(
                    base64_authorization_header, validate=True)
                return decoded_bytes.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None
        return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts user credentials from a Base64 decoded authorization header.

        Args:
            decoded_base64_authorization_header (str): The decoded Base64

        Returns:
            Tuple[Optional[str], Optional[str]]: The user email and password
        """
        if isinstance(decoded_base64_authorization_header, str):
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            match = re.fullmatch(
                pattern, decoded_base64_authorization_header.strip())
            if match:
                user = match.group('user')
                password = match.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> Optional[TypeVar('User')]:
        """
        Retrieves a user object based on authentication credentials.

        Args:
            user_email (str): The user's email address.
            user_pwd (str): The user's password.

        Returns:
            Optional[TypeVar('User')]: The User object if authentication
        """
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            try:
                users = User.search({'email': user_email})
                if not users:
                    return None
                if users[0].is_valid_password(user_pwd):
                    return users[0]
            except Exception:
                return None
        return None

    def current_user(self, request=None) -> Optional[TypeVar('User')]:
        """
        Retrieves the current user from a request.

        Args:
            request: The Flask request object.

        Returns:
            Optional[TypeVar('User')]: The User object if authentication
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        if b64_auth_token is None:
            return None
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        if auth_token is None:
            return None
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
