#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import socket

target_host = "google.com"
target_port = 80

# Criar um objeto de socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar o cliente
client.connect((target_host, target_port))

# Enviar alguns dados
request = "GET / HTTP/1.1\r\nHost: " + target_host + "\r\n\r\n"
client.send(request.encode('utf-8'))

# Receber alguns dados
response = client.recv(4096)

print(response)
