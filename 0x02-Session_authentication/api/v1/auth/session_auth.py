#!/usr/bin/env python3
"""
Module for handling user authentication views.
"""
import os
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session():
    """
    Handle user login.

    Request body (form data):
        - email: The user's email address.
        - password: The user's password.

    Returns:
        - JSON representation of the authenticated user.
        - 400 error if email or password is missing.
        - 404 error if no user is found with the given email.
        - 401 error if the password is incorrect.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            resp = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME')
            resp.set_cookie(session_name, session_id)
            return resp

    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def handle_logout():
    """
    Handle user logout.

    Returns:
        - Empty JSON respocode 200 if the session was successfully destroyed.
        - 404 error if the session could not be destroyed.
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
