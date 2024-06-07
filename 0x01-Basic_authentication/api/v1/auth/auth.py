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
        if (path is None or excluded_paths is None or excluded_paths == []):
            return True
        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path[-1] != '/':
                excluded_path += '/'
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ auth header from req"""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ return the authorization_header """
        return None
