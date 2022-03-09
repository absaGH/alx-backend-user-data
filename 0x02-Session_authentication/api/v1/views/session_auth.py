#!/usr/bin/env python3
""" Module to handle all routes for Session Auth
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Retrieve User instance based on email
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})

    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    for u in user:
        if u.is_valid_password(password):

            from api.v1.app import auth

            sessionID = auth.create_session(user_id=u.id)
            response = jsonify(u.to_json())
            response.set_cookie(getenv('SESSION_NAME'), sessionID)
            return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """ handle DELETE /api/v1/auth_session/logout
    """

    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        abort(404)
