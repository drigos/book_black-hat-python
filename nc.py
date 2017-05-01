#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import getopt
import os
import platform
import socket
import subprocess
import sys
import threading


listen = False
command = False
upload = ""
execute = ""
target = ""
port = 0


def usage():
    print("Net Tool")
    print()
    print("Usage: nc.py -t target_addr -p target_port")
    print("-l --listen              - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run - execute the given file upon receiving a connection")
    print("-c --command             - initialize a command shell")
    print("-u --upload=destination  - upon receiving connection upload a file and write to [destination]")
    print()
    print()
    print("Examples")
    print("nc.py -t 192.168.0.1 -p 5555 -l -c")
    print("nc.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("nc.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'ABCDEFGHI' | nc.py -t 192.168.11.12 -p 135")
    sys.exit(0)


def main():
    global listen
    global command
    global upload
    global execute
    global target
    global port

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hlcu:e:t:p:", [
            "help", "listen", "command", "upload", "execute", "target", "port"
        ])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-l", "--listen"):
            listen = True
        elif opt in ("-c", "--command"):
            command = True
        elif opt in ("-u", "--upload"):
            upload = arg
        elif opt in ("-e", "--execute"):
            execute = arg
        elif opt in ("-t", "--target"):
            target = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        else:
            assert False, "Unhandled option"

    if not listen and len(target) and port > 0:
        client_loop()

    if listen:
        server_loop()


def client_loop():
    print("Modo: client")


def server_loop():
    print("Modo: server")

    global target
    global port

    if not len(target):
        target = "0.0.0.0"

    print((target, port))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((target, port))
    server.listen(5)

    while True:
        socket_fd, socket_str = server.accept()
        client_thread = threading.Thread(target=client_handler, args=(socket_fd,))
        client_thread.daemon = True  # Remove as child threads ao pressionar ctrl-c
        client_thread.start()


def client_handler(client):
    global command
    global upload
    global execute

    if command:
        with client:
            prompt = "".join([os.getlogin(), "@", platform.node(), "> "]).encode("utf-8")
            exit_cmd = b"exit\n"
            client.send(prompt)
            cmd_buffer = recv_until_newline(client)
            while cmd_buffer and not cmd_buffer == exit_cmd:
                output = run_command(cmd_buffer)
                client.send(output + prompt)
                cmd_buffer = recv_until_newline(client)

    elif len(upload):
        file_buffer = recv_all(client)

        try:
            with open(upload, "wb") as file_descriptor:
                file_descriptor.write(file_buffer)
        except IOError as err:
            print(str(err))

    elif len(execute):
        with client:
            output = run_command(execute)
            client.send(output)

    else:
        request = recv_until_newline(client)
        while request:
            print(str(threading.get_ident()) + ": " + request.decode("utf-8")[:-1])
            client.send(b"[ack]\r\n")
            request = recv_until_newline(client)


def run_command(command):
    command = command.rstrip()

    try:
        output = subprocess.check_output(command.decode("utf-8"),
                                         stderr=subprocess.STDOUT,
                                         shell=True)
        # NOTE (rodrigo:2017-05-01): Python 3.5
        # output = subprocess.run(command, check=True, shell=True,
        #                         stdout=subprocess.PIPE,
        #                         stderr=subprocess.STDOUT).stdout
    except subprocess.CalledProcessError as err:
        output = "".join([str(err), "\n"]).encode("utf-8")

    return output


# http://stackoverflow.com/questions/667640/how-to-tell-if-a-connection-is-dead-in-python#667710

def recv_until_newline(socket):
    data = b''
    chunk = b''

    while b'\n' not in chunk:
        chunk = socket.recv(5)
        if not chunk:
            break
        data += chunk

    return data


def recv_n_bytes(socket, n_bytes):
    data = b''

    while len(data) < n_bytes:
        chunk = socket.recv(n_bytes - len(data))
        if not chunk:
            break
        data += chunk

    return data


def recv_all(socket):
    data = b''

    while True:
        chunk = socket.recv(5)
        if not chunk:
            break
        data += chunk

    return data


main()
