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
        if (path is None or excluded_paths is None or not excluded_paths):
            return True
        if not path.endswith('/'):
            path += '/'
        excluded_paths = [item if item.endswith(
            '/') else item + '/' for item in excluded_paths]
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ auth header from req"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ return the authorization_header """
        return None
