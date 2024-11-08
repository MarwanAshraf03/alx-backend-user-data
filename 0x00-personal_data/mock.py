#!/usr/bin/env python3
import re
message = "name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;"
new_message = re.sub(";date_of_birth=(.*?);", r";password=xxx;", message)
print(new_message)