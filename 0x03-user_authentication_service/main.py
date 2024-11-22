#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

user = auth.register_user(email, password)
user2 = auth.register_user("email", password)
user3 = auth.register_user("email2", password)

print(auth.create_session(email))
print(auth.create_session("email2"))
print(auth.create_session("unknown@email.com"))

print(auth.get_user_from_session_id(user.session_id))
print(auth.get_user_from_session_id(user.session_id).id)
print(auth.get_user_from_session_id(user2.session_id))
print(auth.get_user_from_session_id(user3.session_id))
print(auth.get_user_from_session_id(user3.session_id).id)
