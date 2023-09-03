"""
title           : serPBB.py 
description     : A server that implements a PBB (Public Bulletin 
                : Board). It can establish a secure chan over ssl
                : with clients and execute requests to post and
                : retrieve tokens. 
                :
                : I created the self-signed certificates following the steps
                : https://github.com/mikepound/tls-exercises/tree/master/ca
                : 
inspiration     : https://github.com/mikepound/tls-exercises
source          :
                : 
author          : Carlos Molina-Jimenez
                : carlos.molina@cl.cam.ac.uk
                : 2 Sep 2023, Computer Lab, University of Cambridge
date            : 3 Sep 2023
version         : __ 
                : Save to file and sign of responses not
                : implemented yet. 
usage           : 
notes           :
compile and run : % python3 serPBB.py 
                : The program expects ca.cert in ./resources/server, 
                : that is, in a folder called client located in the
                : parent folder.
                :
                : % python3 serPBB.p
                : PBB Server listening on port 8282...
                : 
                : % python3 serPBB.py -s localhost -p 8280
                : PBB Server listening on port 8280...
                :
python_version  : Python 3.7.4 (v3.7.4:e09359112e, Jul 8 2019)      
"""

import socket
import ssl
import threading
from pathlib import Path
import select

import tqdm
import os

import pickle

from files2sockets import recvpicklemsg, sendpicklemsg


LOCAL_HOST = 'localhost'
LOCAL_PORT = 8282
RESOURCE_DIRECTORY = Path(__file__).resolve().parent / 'certskeys' / 'server'
SERVER_CERT_CHAIN = RESOURCE_DIRECTORY / 'pbbServer.intermediate.chain.pem'
SERVER_KEY = RESOURCE_DIRECTORY / 'pbbServer.key.pem'


# three new lines 
# receive 4096 bytes each time
BUFFER_SIZE = 4096


class ServerPBB():

    def __init__(self, server=LOCAL_HOST, port=LOCAL_PORT):
        """
        Creates an SSLContext: provides params for any future SSL connections
        """
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=SERVER_CERT_CHAIN, keyfile=SERVER_KEY)
        self.context = context
        self.server  = server 
        self.port    = port 
        self.pbbrecords= [] # a list to hold posted tokens
                            # It is only in memory. I need to persist it 
                            # on disk

    def start_server(self):
        """
        Begins listening on a socket. Any connections that arrive 
        are wrapped in an SSLSocket using the context created 
        during initialisation

        Makes use of the OS select function to perform basic non-blocking IO. 
        Once a connection has established
        an instance of ClientHandler is created to serve the client
        """

        server_socket = socket.socket()
        server_socket.bind((self.server, self.port))
        server_socket.listen(5)
        read_list = [server_socket]

        print("PBB Server listening on port {0}...".format(self.port))
        print("PBB Server operating with openssl version: ", ssl.OPENSSL_VERSION) 

        while True:
            readable, writable, errored = select.select(read_list, [], [], 2)
            for s in readable:
                if s is server_socket:
                    client_socket, address = server_socket.accept()
                    try:
                        # Wrap the socket in an SSL connection (will perform a handshake)
                        conn = self.context.wrap_socket(client_socket, server_side=True)
                        ClientHandler(conn, self.pbbrecords).start()
                        ###server_socket.close()   # close the server socket or hang
                    except ssl.SSLError as e:
                        print(e)


class ClientHandler(threading.Thread):
    """
    Thread handler leaves the main thread free to handle any other incoming connections
    """
    def __init__(self, conn, pbbrecrds):
        threading.Thread.__init__(self)
        print("init of Client handler has been called")
        self.conn      = conn
        self.pbbrecrds = pbbrecrds 
        print("init of Client handler has completed")


    def run(self):
        try:
            # Read up to 4x1024 bytes from the client

            print("Ser: hiiiiiiiiiiiiiiii before calling recvpicklemsg")
            list= recvpicklemsg(self.conn, 10)
            print("Ser: heeee after calling recvpicklemsg")
            
            sendpicklemsg(self.conn, list, 10, self.pbbrecrds)
            print("heeee after calling sendpicklemsg")

        except ssl.SSLError as e:
            print(e)
        except Exception as e:
            print(e)
        finally:
            self.conn.close()
            print("ser_PBB.py waiting for requests ...")


def main():
   import argparse
   parser = argparse.ArgumentParser(description="A server implementing a PBB with sec chan")
   parser.add_argument("-s", "--server", help="Server implementing the PBB, default is local host", default= "localhost")
   parser.add_argument("-p", "--port", help="Port to use, default is 8282", default=8282)

   args    = parser.parse_args()
   server  = args.server
   port    = args.port

   pbbser = ServerPBB(server, int(port))
   pbbser.start_server()

if __name__ == '__main__':
    main()
