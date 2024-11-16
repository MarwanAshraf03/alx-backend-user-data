#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    user_email = request.form.get("email")
    user_pwd = request.form.get("password")
    if user_email is None or user_email == "":
        return jsonify({"error": "email missing"}), 400
    if user_pwd is None or user_pwd == "":
        return jsonify({"error": "password missing"}), 400
    from models.user import User
    try:
        user_list = User.search({"email": user_email})
    except KeyError:
        return jsonify({"error": "no user found for this email"}), 404
    user = None
    for i in user_list:
        if user_email in i.__dict__.values():
            user = i
    if user is None:
        return jsonify({"error": "no user found for this email"}), 404
    if not user.is_valid_password(user_pwd):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    print(session_id)
    print(auth.session_cookie(request))
    return user.to_json()
