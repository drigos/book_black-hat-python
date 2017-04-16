#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import socket
import threading


bind_addr = "0.0.0.0"
bind_port = 9999


def handle_client(client_socket):
    with client_socket:
        request = client_socket.recv(1024)
        print("Received: {}".format(request.decode()))
        client_socket.send(b"ACK!")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((bind_addr, bind_port))
    s.listen(5)
    print("Listenin on {}:{}".format(bind_addr, bind_port))

    while True:
        socket_fd, socket_str = s.accept()
        print("Accepted connection from {}:{}".format(socket_str[0], socket_str[1]))
        client_handler = threading.Thread(target=handle_client, args=(socket_fd,))
        client_handler.start()
