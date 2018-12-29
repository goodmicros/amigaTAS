#!/usr/bin/python3

import serial
import sys
import time

TAS = serial.Serial(sys.argv[1], baudrate = 115200)

#capture data and log it as events
starttime = time.time()
while(True):
    data = TAS.read(1)
    now = time.time() - starttime 
    with open('./output', 'a') as f:
        f.write(str(now) + ' ' + data.hex() + '\n')
    

