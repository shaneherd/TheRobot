#!/usr/bin/env python
import serial
import time
import sys

#0.4 m/s @ speed = 100

def setSpeed(ser, motor, direction, speed):
    if motor == 1 and direction == 0:
        sendByte = chr(0xC2)
    if motor == 0 and direction == 0:
        sendByte = chr(0xCA)
    if motor == 1 and direction == 1:
        sendByte = chr(0xC1)
    if motor == 0 and direction == 1:
        sendByte = chr(0xC9)

    ser.write(sendByte)
    ser.write(chr(speed))

ser = serial.Serial('/dev/ttyUSB1', 19200, timeout = 1)
d = sys.argv[2]
dist = float(d)
#sleepTime = dist / 0.4
sleepTime = dist
if (sys.argv[2] == '1'):
    if sys.argv[1] == 'r':
        setSpeed(ser, 0, 1, 100)
        setSpeed(ser, 1, 0, 100)
        time.sleep(0.5)
        setSpeed(ser, 0, 1, 0)
        setSpeed(ser, 1, 0, 0)
    if sys.argv[1] == 'l':
        setSpeed(ser, 0, 0, 100)
        setSpeed(ser, 1, 1, 100)
        time.sleep(0.5)
        setSpeed(ser, 0, 0, 0)
        setSpeed(ser, 1, 1, 0)
    if sys.argv[1] == 'f':
        setSpeed(ser, 0, 0, 100)
        setSpeed(ser, 1, 0, 100)
    if sys.argv[1] == 'b':
        setSpeed(ser, 0, 1, 100)
        setSpeed(ser, 1, 1, 100)
else:
    setSpeed(ser, 0, 1, 0)
    setSpeed(ser, 1, 1, 0)
ser.close()
