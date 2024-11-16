#!/usr/bin/env python3
from datetime import datetime
from time import sleep
first = datetime.now()
sleep(3)
second = datetime.now()
print(first)
print(second)
print(second-first)
print(type(second-first))
print((second-first).seconds)
