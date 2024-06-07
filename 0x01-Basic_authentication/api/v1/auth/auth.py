#!/usr/bin/env python3
"""
Route module for the API
"""

from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """ class to manage API """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if auth is requred for path """
        if path is None or not excluded_paths:
            return True

        if path[-1] == '/' and path != '/':
            path = path[:-1]

        for excluded_path in excluded_paths:
            if excluded_path[-1] == '/' and excluded_path != '/':
                excluded_path = excluded_path[:-1]

            if fnmatch.fnmatch(path, excluded_path):
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
