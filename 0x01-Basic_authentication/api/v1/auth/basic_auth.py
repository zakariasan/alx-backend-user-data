#!/usr/bin/env python3
"""
Route module for the API
"""

from api.v1.auth.auth.py import Auth


class BasicAuth(Auth):
    """Basic authentication class that inherits from Auth."""
    pass
