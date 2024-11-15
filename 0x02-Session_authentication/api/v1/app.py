#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
authS = {
    "basic_auth": BasicAuth,
    "session_auth": SessionAuth,
}
authType = getenv('AUTH_TYPE')
if authType in authS.keys():
    auth = authS[authType]()
else:
    auth = Auth()


@app.before_request
def before():
    """method to act before the request"""
    if auth is not None:
        if not auth.require_auth(request.path, ['/api/v1/status/',
                                                '/api/v1/unauthorized/',
                                                '/api/v1/forbidden/',
                                                "/api/v1/auth_session/login/"
                                                ]):
            return
        if auth.authorization_header(request) is None\
                and auth.session_cookie(request) is None:
            print(1)
            abort(401)
        # if auth.authorization_header(request) is None:
        #     print(2)
        #     abort(401)
        if auth.current_user(request) is None:
            print(3)
            abort(403)
    else:
        pass
    request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    print(auth)
    print(auth)
    app.run(host=host, port=port, debug=True)