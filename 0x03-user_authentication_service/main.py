#!/usr/bin/env python3
"""
Main file
"""
from user import User
import requests
from json import loads, dumps


def register_user(email: str, password: str) -> None:
    """function documentation"""
    params = {
        "email": email,
        "password": password
    }
    resp = requests.post("http://192.168.42.171:5000/users", data=params)
    assert b'{"email":"guillaume@holberton.io","message":"user created"}\n'\
        == resp.content


def log_in_wrong_password(email: str, password: str) -> None:
    """function documentation"""
    params = {
        "email": email,
        "password": password
    }
    resp = requests.post("http://192.168.42.171:5000/sessions", data=params)
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """function documentation"""
    params = {
        "email": email,
        "password": password
    }
    resp = requests.post("http://192.168.42.171:5000/sessions", data=params)
    assert resp.content ==\
        b'{"email":"guillaume@holberton.io","message":"logged in"}\n'
    return resp.cookies.get("session_id")


def profile_unlogged() -> None:
    """function documentation"""
    resp = requests.get("http://192.168.42.171:5000/profile")
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """function documentation"""
    resp = requests.get("http://192.168.42.171:5000/profile",
                        cookies={"session_id": session_id})
    assert resp.content == b'{"email":"guillaume@holberton.io"}\n'


def log_out(session_id: str) -> None:
    """function documentation"""
    resp = requests.delete("http://192.168.42.171:5000/sessions",
                           cookies={"session_id": session_id})
    assert resp.content == b'{"message":"Bienvenue"}\n'


def reset_password_token(email: str) -> str:
    """function documentation"""
    resp = requests.post("http://192.168.42.171:5000/reset_password",
                         data={"email": email})
    token = loads(resp.content.decode('utf-8'))['reset_token']
    asserting = {"email": f"{email}", "reset_token": f"{token}"}
    asserting = dumps(asserting)
    asserting += "\n"
    asserting = asserting.replace(" ", "")
    asserting = bytes(asserting, encoding='utf-8')
    assert resp.content == asserting
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """function documentation"""
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password,
    }
    resp = requests.put("http://192.168.42.171:5000/reset_password", data=data)
    assert resp.content ==\
        b'{"email":"guillaume@holberton.io","message":"Password updated"}\n'


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    """"""
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
