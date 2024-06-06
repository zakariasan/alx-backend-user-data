#!/usr/bin/env python3
"""
Route module for the API
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ class to manage API """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if auth is requred for path """
        return False

    def authorization_header(self, request=None) -> str:
        """ auth header from req"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ return the authorization_header """
        return None
