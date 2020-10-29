# -*- coding: utf-8 -*-

import socket
import serial
import pygame
import time


# Declaramos las variables
ipServidor = "192.168.100.135"
puertoServidor = 1922

# Configuramos los datos para conectarnos con el servidor
# socket.AF_INET para indicar que utilizaremos Ipv4
# socket.SOCK_STREAM para utilizar TCP/IP (no udp)
# Estos protocolos deben ser los mismos que en el servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((ipServidor, puertoServidor))
print("Conectado con el servidor ---> %s:%s" % (ipServidor, puertoServidor))

pygame.init()
# Define a joystick object to read from
j = pygame.joystick.Joystick(0)
# Initiate the joystick or controller
j.init()
# Print the name of any detected controllers
print 'Detected controller : %s' % j.get_name()

axes_to_check = [4, 2]
check_frequency = 5
breakout_button = 3

t_button = 0
o_button = 1
x_button = 2
l1_button = 4
l2_button = 6
r1_button = 5
r2_button = 7
start_button = 9
select_button = 8

EST_ANX = 0
FLAGX = 0
EST_ANR2 = 0
FLAGR2 = 0
EST_ANO = 0
FLAGO = 0

while True:
    pygame.event.pump()
    recent_values = []
    recent_values1 = []
    for current_axis in axes_to_check:
        latest_value = j.get_axis(current_axis)
        value_mod = int(round(latest_value*100, 1)+100)
        value_mod = str(value_mod)
        recent_values.append(value_mod)

    serial_output = ','.join(recent_values) + ';'

    if j.get_button(select_button) == 1:
        break

    if j.get_button(r1_button) == 1:
        cliente.send("R1,")
        print("R1")

    if j.get_button(r1_button) == 1 and j.get_button(r2_button) == 1:
        cliente.send("R2,")

    if j.get_button(r2_button) == 1 and EST_ANR2 == 0:
        EST_ACR2 = 1

        if FLAGR2 == 0:
            cliente.send('Q,')
            print("R2 - ENCENDER")
            FLAGR2 = 1

        elif FLAGR2 == 1:
            cliente.send('W,')
            print("R2 - APAGAR")
            FLAGR2 = 0

    if j.get_button(r2_button) == 0:
        EST_ACR2 = 0

    EST_ANR2 = EST_ACR2

    if j.get_button(x_button) == 1 and EST_ANX == 0:
        EST_ACX = 1

        if FLAGX == 0:
            cliente.send('A,')
            print("***************** DISPARADOR ENCENDIDO *****************")
            print("***************** DISPARADOR ENCENDIDO *****************")
            print("***************** DISPARADOR ENCENDIDO *****************")
            print("***************** DISPARADOR ENCENDIDO *****************")
            print("***************** DISPARADOR ENCENDIDO *****************")
            FLAGX = 1

        elif FLAGX == 1:
            cliente.send('B,')
            print("+++++++++++++++++ DISPARADOR APAGADO +++++++++++++++++++")
            print("+++++++++++++++++ DISPARADOR APAGADO +++++++++++++++++++")
            print("+++++++++++++++++ DISPARADOR APAGADO +++++++++++++++++++")
            print("+++++++++++++++++ DISPARADOR APAGADO +++++++++++++++++++")
            print("+++++++++++++++++ DISPARADOR APAGADO +++++++++++++++++++")
            FLAGX = 0

    if j.get_button(x_button) == 0:
        EST_ACX = 0

    EST_ANX = EST_ACX

    if j.get_button(l1_button) == 1:
        cliente.send('L1,')

    if j.get_button(l2_button) == 1:
        cliente.send('L2,')

    if j.get_button(start_button) == 1:
        cliente.send('ST,')

    if j.get_button(o_button) == 1 and EST_ANO == 0:
        EST_ACO = 1

        if FLAGO == 0:
            cliente.send('C,')
            print("***************** RECOLECTOR ENCENDIDO *****************")
            print("***************** RECOLECTOR ENCENDIDO *****************")
            print("***************** RECOLECTOR ENCENDIDO *****************")
            print("***************** RECOLECTOR ENCENDIDO *****************")
            print("***************** RECOLECTOR ENCENDIDO *****************")
            FLAGO = 1

        elif FLAGO == 1:
            cliente.send('D,')
            print("+++++++++++++++++ RECOLECTOR APAGADO +++++++++++++++++++")
            print("+++++++++++++++++ RECOLECTOR APAGADO +++++++++++++++++++")
            print("+++++++++++++++++ RECOLECTOR APAGADO +++++++++++++++++++")
            print("+++++++++++++++++ RECOLECTOR APAGADO +++++++++++++++++++")
            print("+++++++++++++++++ RECOLECTOR APAGADO +++++++++++++++++++")
            FLAGO = 0

    if j.get_button(o_button) == 0:
        EST_ACO = 0

    EST_ANO = EST_ACO

    cliente.send(serial_output)

    respuesta = cliente.recv(4096)
    print(respuesta)
    if respuesta == "exit":
        break


print("------- CONEXIÓN CERRADA ---------")
cliente.close()
