#!/usr/bin/env python3
""" Module that defines routes for session login """
from api.v1.views import app_views
from flask import abort, jsonify, request, session
from models.user import User
import os


@app_views.route(
    '/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """ view that handles all routes for the Session authentication """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        user = User.search({'email': email})
    except Exception:
        user = None

    if user:
        validate_password = user[0].is_valid_password(password)
        if not validate_password:
            return jsonify({"error": "wrong password"}), 401
        from api.v1.app import auth
        session_id = auth.create_session(user[0].id)
        user_dict = jsonify(user[0].to_json())
        cookie = os.getenv('SESSION_NAME')
        user_dict.set_cookie(cookie, session_id)
        return user_dict
    else:
        return jsonify({"error": "no user found for this email"}), 404


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout_session() -> str:
    """ delete session (logout) """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
