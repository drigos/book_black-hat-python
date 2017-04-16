#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

target_host = "127.0.0.1"
target_port = 80

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b"AAABBBCCC\n", (target_host, target_port))
    response, addr = s.recvfrom(4096)

print(addr)
print(response)
