#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
import os

from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = getenv('AUTH_TYPE', 'auth')
if auth_type == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth(403)


@app.errorhandler(403)
def forbidden(error):
    """Forbidden handler."""
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(401)
def unauthorized(error):
    """Unauthorized handler."""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404

@app.before_request
def auth_user():
    """ auth a user before processing """
    if auth is None:
        return
    bad_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
    ]
    if not auth.require_auth(request.path, bad_paths) is None:
        abort(401)

    if auth.authorization_header(request) is None:
        abort()
if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
