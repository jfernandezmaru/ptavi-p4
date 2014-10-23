#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion" + '\r\n')

        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            #print("envio ------> " + str(line[0]))
            line = self.rfile.read()
            lista= line.split(" ")

            if lista[0] == 'REGISTER':

                Nick = lista[1].split(":")
                Dic_clients[Nick[1]]= self.client_address[0]
                print ("Cliente Registrado")
                print 'El cliente nos manda: ' + line
                self.wfile.write("SIP/2.0 200 OK" + '\r\n')
            if not line:
            
                break

if __name__ == "__main__":

    # Creamos servidor de eco y escuchamos
    PORT = int(sys.argv[1])
    Dic_clients ={}
    serv = SocketServer.UDPServer(("", PORT), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
