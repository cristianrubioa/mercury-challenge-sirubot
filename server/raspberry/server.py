# -*- coding: utf-8 -*-

import socket
import serial
import os
import time
import sys
from flask import Flask, render_template, request, redirect, url_for, make_response
import subprocess
import RPi.GPIO as GPIO

Relay_Ch2 = 20

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(Relay_Ch2, GPIO.OUT)
GPIO.output(Relay_Ch2, GPIO.HIGH)

# ...Crea un objeto de puerto serie
SerialPort = serial.Serial('/dev/ttyACM0', 115200)  # port.ino
SerialDis = serial.Serial('/dev/ttyUSB0', 115200)  # disp.ino

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('google.com', 80))
ipAddress = s.getsockname()[0]
s.close()
mensaje = "La direccion ip es: " + ipAddress
print(mensaje)

ip = str(ipAddress)
puerto = 1922
dataConection = (ip, puerto)
conexionesMaximas = 2

# Creamos el servidor.
socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se Asigna los valores del servidor
socketServidor.bind(dataConection)

# Se Asigna el número máximo de conexiones
socketServidor.listen(conexionesMaximas)

print("Esperando conexiones en: %s:%s" % (ip, puerto))
cliente, direccion = socketServidor.accept()
print("Conexion establecida con: %s:%s" % (direccion[0], direccion[1]))


# Bucle de escucha. En él indicamos la forma de actuar al recibir los datos del cliente
while True:
    # El número indica el número maximo de bytes
    datos = cliente.recv(5000)

    D = datos.split(",")

    if len(D) >= 2:
        D.append("0")
        D.append("0")

    if D[0] == 'R1' and D[1] == 'R2':
        SerialPort.write(D[2] + "," + D[3] + "1" + ":")
    else:
        SerialPort.write("90,90;0:")

    if D[0] == 'R1' and D[3] == '0':
        SerialPort.write(D[1] + "," + D[2] + "0" + ":")

    if D[0] == 'L1':
        SerialDis.write(D[1] + "," + D[2] + "1" + ":")

    else:
        SerialDis.write("90,90;1:")

    if D[0] == 'L2':
        SerialDis.write(D[1] + "," + D[2] + "0" + ":")

    if D[0] == 'ST':
        SerialDis.write("89,89;3:")

    if D[0] == 'Q':
        GPIO.output(Relay_Ch2, GPIO.LOW)

    if D[0] == 'W':
        GPIO.output(Relay_Ch2, GPIO.HIGH)

    if D[0] == 'A':
        SerialDis.write("91,91;3:")

    if D[0] == 'B':
        SerialDis.write("92,92;3:")

    if D[0] == 'C':
        SerialPort.write("91,91;0:")

    if D[0] == 'D':
        SerialPort.write("92,92;0:")

    if datos == "exit":
        cliente.send("exit")
        break

    print("RECIBIDO: %s" % D)
    cliente.sendall("-- Recibido --")


print("------- CONEXIÓN CERRADA ---------")
socketServidor.close()
