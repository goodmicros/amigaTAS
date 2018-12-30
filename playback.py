#!/usr/bin/python3

import serial
import sys
import time

TAS = serial.Serial(sys.argv[1], baudrate = 115200)

#just read the whole file into memory?
with open('./output', 'r') as f:
    lines = f.read().split('\n')

#try to accurately repeat the events
starttime = time.time()
for line in lines:
    timestamp, data = line.split(' ')
    try:
        time.sleep(float(timestamp) - (time.time() - starttime))
    except:
        pass
    TAS.write(bytes.fromhex(data))
