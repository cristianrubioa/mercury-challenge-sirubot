# -*- coding: utf-8 -*-

import serial
import os
import time
import sys
import RPi.GPIO as GPIO

response = 0


def pingRed():
    IP = 'google.com'
    response = os.system("ping -c 1 " + IP)

    if response == 0:
        print("La red: " + str(IP) + " esta lista ")
    else:
        GPIO.output(Relay_Ch2, GPIO.LOW)
        time.sleep(0.3)
        GPIO.output(Relay_Ch2, GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(Relay_Ch2, GPIO.LOW)

        print("********* La red no esta disponible ********* ")


while True:
    try:
        pingRed()
    except KeyboardInterrupt:
        print "Connection failed"
