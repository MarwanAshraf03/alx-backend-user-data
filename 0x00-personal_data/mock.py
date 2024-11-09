#!/usr/bin/env python3
import datetime


ll = ["name", "email", "phone", "ssn", "password", "ip", "last_login", "user_agent"]
tt = ('Marlene Wood', 'hwestiii@att.net', '(473) 401-4253', '261-72-6780', 'K5?BMNv', '60ed:c396:2ff:244:bbd0:9208:26f2:93ea', datetime.datetime(2019, 11, 14, 6, 14, 24), 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36')
print(";".join([f"{i}={j}" for i, j in zip(ll, tt)]))