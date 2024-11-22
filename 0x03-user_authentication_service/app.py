#!/usr/bin/env python3
"""flask app module"""
from flask import jsonify, Flask, request, abort
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
