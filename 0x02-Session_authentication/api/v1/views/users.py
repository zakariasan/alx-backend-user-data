#!/usr/bin/env python3
"""
Module for handling user-related routes.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """
    GET /api/v1/users
    Retrieves a list of all User objects.

    Returns:
        - JSON representation of all User objects.
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """
    GET /api/v1/users/:id
    Retrieves a User object by ID.

    Path parameter:
        - user_id (str): The ID of the User to retrieve.

    Returns:
        - JSON representation of the User object.
        - 404 error if the User ID doesn't exist.
    """
    if user_id is None:
        abort(404)
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_json())
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """
    DELETE /api/v1/users/:id
    Deletes a User object by ID.

    Path parameter:
        - user_id (str): The ID of the User to delete.

    Returns:
        - Empty JSON response with status code 200 if the User was successfully deleted.
        - 404 error if the User ID doesn't exist.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """
    POST /api/v1/users/
    Creates a new User object.

    JSON body:
        - email (str): The email of the new User.
        - password (str): The password of the new User.
        - first_name (str, optional): The first name of the new User.
        - last_name (str, optional): The last name of the new User.

    Returns:
        - JSON representation of the new User object with status code 201.
        - 400 error if the User cannot be created.
    """
    try:
        rj = request.get_json()
        if not rj:
            raise ValueError("Wrong format")
        if not rj.get("email"):
            raise ValueError("email missing")
        if not rj.get("password"):
            raise ValueError("password missing")

        user = User()
        user.email = rj.get("email")
        user.password = rj.get("password")
        user.first_name = rj.get("first_name")
        user.last_name = rj.get("last_name")
        user.save()
        return jsonify(user.to_json()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Can't create User: {e}"}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """
    PUT /api/v1/users/:id
    Updates an existing User object by ID.

    Path parameter:
        - user_id (str): The ID of the User to update.

    JSON body:
        - first_name (str, optional): The new first name of the User.
        - last_name (str, optional): The new last name of the User.

    Returns:
        - JSON representation of the updated User object.
        - 404 error if the User ID doesn't exist.
        - 400 error if the update fails due to wrong format.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)

    try:
        rj = request.get_json()
        if not rj:
            raise ValueError("Wrong format")

        if rj.get('first_name') is not None:
            user.first_name = rj.get('first_name')
        if rj.get('last_name') is not None:
            user.last_name = rj.get('last_name')

        user.save()
        return jsonify(user.to_json()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Can't update User: {e}"}), 400
