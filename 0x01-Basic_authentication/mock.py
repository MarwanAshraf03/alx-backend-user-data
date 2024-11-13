#!/usr/bin/env python3
excluded_paths = ['/api/v1/status', '/api/v1/unauthorized/', '/api/v1/forbidden/']
path = "/api/v1/users/"
print([i.replace("*", "") in path for i in excluded_paths])
path = "/api/v1/status/"
print([i.replace("*", "") in path for i in excluded_paths])
path = "/api/v1/stats/"
print([i.replace("*", "") in path for i in excluded_paths])