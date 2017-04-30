#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import getopt
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

    print("listen:", listen)
    print("command:", command)
    print("upload:", upload)
    print("execute:", execute)
    print("target:", target)
    print("port:", port)


main()
