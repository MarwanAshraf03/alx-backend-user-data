#!/usr/bin/env python3
"""flask app module"""
from flask import jsonify, Flask, request, abort, redirect
from auth import Auth
AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'])
def get_route():
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email=email, password=password)
        return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        ret = jsonify({"email": f"{email}", "message": "logged in"})
        ret.set_cookie("session_id", session_id)
        return ret
    else:
        abort(401)


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    else:
        AUTH.destroy_session(user.id)
        return redirect("/")


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile():
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    else:
        return jsonify({"email": f"{user.email}"})


@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email=email)
        return jsonify({"email": f"{email}", "reset_token": f"{reset_token}"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
