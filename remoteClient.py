#!/usr/bin/python3

import serial
import sys
import socket

#setup socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((sys.argv[1], 1985))

#send input to server
data = b'\xff'
server.sendall(data)
server.close()
