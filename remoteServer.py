#!/usr/bin/python3

import serial
import sys
import socket

#connect to controller
TAS = serial.Serial(sys.argv[1], baudrate = 115200)

#setup socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 1985))
server.listen(1)

#wait for client
client, address = server.accept()

#repeat client inputs
while True:
    data = client.recv(1)
    TAS.write(data)
