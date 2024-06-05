#!/usr/bin/env python3
""" Module of Index views
"""
#!/usr/bin/env python3
"""
Module of Index views
"""


# Route to handle unauthorized access




from flask import jsonify, abort
from api.v1.views import app_views
@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def authorized() -> str:
    """
    GET /api/v1/unauthorized
    Return:
        - raises a 401 error (Unauthorized)
    """
    abort(401, description="Unauthorized")

# Route to handle forbidden access


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbid() -> str:
    """
    GET /api/v1/forbidden
    Return:
        - raises a 403 error (Forbidden)
    """
    abort(403, description="Forbidden")

# Route to check the status of the API


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
    GET /api/v1/status
    Return:
        - JSON status of the API
    """
    return jsonify({"status": "OK"})

# Route to get statistics of the objects


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """
    GET /api/v1/stats
    Return:
        - JSON stats of the objects
    """
    from models.user import User  # Import here to avoid circular import issues
    stats = {}
    stats['users'] = User.count()  # Count number of users
    return jsonify(stats)
