#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# Practica 4 Javier Fernandez Marugan  PTAVI
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

try:
    """
    Intentamos construir el Cliente UDP simple y Dirección IP del servidor
    cerciorándonos previamente de que el EXPIRES es mayor o igual a cero y
    que está escrita correctamente la palabra register
    """
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    REGISTER = sys.argv[3].upper()
    EXPIRES = int(sys.argv[5])
    if EXPIRES < 0:
        sys.exit("Usage: expires_value need to be at least 0")
except ValueError:
    print "Usage: client.py ip puerto register sip_address expires_value"

# Contenido que vamos a enviar
LINE = sys.argv[4:]
LINE = " ".join(LINE)

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))
print "Enviando: " + LINE
my_socket.send(REGISTER + ' sip:' + LINE + ' SIP/2.0' + '\r\n''\r\n')
data = my_socket.recv(1024)
print "Recibido -- ", data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
