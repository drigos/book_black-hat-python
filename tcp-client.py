#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import socket

target_host = "duckduckgo.com"
target_port = 80

# Criar um objeto de socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((target_host, target_port))
    request = "GET / HTTP/1.1\r\nHost: " + target_host + "\r\n\r\n"
    s.sendall(request.encode('utf-8'))
    response = s.recv(4096)

print(response)
