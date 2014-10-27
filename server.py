#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import time

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def register2file (self, client, IP,expire,dictionary):

        fich = open("registered.txt", "r+")
        fich.write("User" + "\t" + "IP" + "\t" + "Expires" + "\n")
        expires= time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(expire))
        fich.write(client + "\t" + IP + "\t" + expires + "\n")
            
    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion" + '\r\n')

        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            lista= line.split(" ")
            
            if line != "":
            
                Nick = lista[1].split(":")
                expire= time.time() + int(lista[2])
                Dic_clients[Nick[1]]= (self.client_address[0], expire)
                
                if lista[0] == 'REGISTER':

                    print ("Cliente Registrado: (" + str(self.client_address[0]) + " , " + str(self.client_address[1]) + ")")
                    print 'El cliente nos manda: ' + line
                    self.wfile.write("SIP/2.0 200 OK" + '\r\n')
                    self.register2file(str(Nick[1]),str(self.client_address[0]),expire,Dic_clients)
                    
                if lista[2] == "0":

                    print ("Cliente dado de baja: (" + str(self.client_address[0]) + " , " + str(self.client_address[1]) + ")")  
                    del Dic_clients[Nick[1]]
                    self.wfile.write("SIP/2.0 200 OK" + '\r\n')
                    self.register2file(str(Nick[1]),str(self.client_address[0]),expire,Dic_clients)
             
                else:
                    
                    now= time.time()

                    if Dic_clients[Nick[1]][1] <= now:

                        print ("Cliente dado de baja: (" + str(self.client_address[0]) + " , " + str(self.client_address[1]) + ")")  
                        del Dic_clients[Nick[1]]
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

