#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys


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


main()
