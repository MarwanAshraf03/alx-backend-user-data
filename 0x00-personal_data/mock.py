#!/usr/bin/env python3
import bcrypt
string = "password"
print(bytes(string, "UTF-8"))
print(b"password")
print(type(b"password"))
print(bcrypt.hashpw(b"password", bcrypt.gensalt()))