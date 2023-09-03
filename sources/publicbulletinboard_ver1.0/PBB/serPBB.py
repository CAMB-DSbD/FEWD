"""
title           : serPBB.py 
description     : A server that implements a PBB (Public Bulletin 
                : Board). It can establish a secure chan over ssl
                : with clients and respont to post token and retrieve
                : tokens  requests placed by clients.
                :
                : Responses to retrieve resquets are sent in 
                : list=[t1, t2, ..., signature, vk]
                :
                : signature is placed on t1<#>t2<#> ... after encoding 
                : it in utf-8 format with the signing key, sk
                : sk = SigningKey.generate(curve=NIST192p)
                : vk = sk.verifying_key but serialised with 
                : vk.to_string() before including in list
                : 
inspiration     : https://github.com/mikepound/tls-exercises
source          :
                : 
author          : Carlos Molina-Jimenez
                : carlos.molina@cl.cam.ac.uk
                : 26 Jul 2023, Computer Lab, University of Cambridge
date            : 11 Jul 2023
version         : 1.0 (not complete yet: 
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
                : It can also be run by calling
                : % python3 test_ServerPBB.py
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
from ecdsa import SigningKey, VerifyingKey, BadSignatureError, NIST192p

LOCAL_HOST = 'localhost'
LOCAL_PORT = 8282
RESOURCE_DIRECTORY = Path(__file__).resolve().parent / 'resources' / 'server'
SERVER_CERT_CHAIN = RESOURCE_DIRECTORY / 'server.intermediate.chain.pem'
SERVER_KEY = RESOURCE_DIRECTORY / 'server.key.pem'


# three new lines 
# receive 4096 bytes each time
BUFFER_SIZE = 4096
HEADER_SIZE = 10


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
        # create sign and verify keys
        self.sk = SigningKey.generate(curve=NIST192p)
        self.vk = self.sk.verifying_key



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
        print("...  using version: ", ssl.OPENSSL_VERSION)
        
        while True:
            readable, writable, errored = select.select(read_list, [], [], 2)
            for s in readable:
                if s is server_socket:
                    client_socket, address = server_socket.accept()
                    try:
                        # Wrap the socket in an SSL connection (will perform a handshake)
                        conn = self.context.wrap_socket(client_socket, server_side=True)
                        ClientHandler(conn, self.pbbrecords, self.sk, self.vk).start()
                        ###server_socket.close()   # close the server socket or hang
                    except ssl.SSLError as e:
                        print(e)


class ClientHandler(threading.Thread):
    """
    Thread handler leaves the main thread free to handle any other incoming connections
    """
    def __init__(self, conn, pbbrecrds, sk, vk):
        threading.Thread.__init__(self)
        print("Client handler has been called ...")
        self.conn      = conn
        self.pbbrecrds = pbbrecrds 
        self.sk= sk
        self.vk= vk
        print("init of Client handler has completed")


    def run(self):
        try:
          # Read up to 4x1024 bytes from the client

          list= recvpicklemsg(self.conn, HEADER_SIZE) # improve: pass headersize in self 
          print("Server has received pickle msg from client")
            
          sendpicklemsg(self.conn, list, HEADER_SIZE, self.pbbrecrds, self.sk, self.vk)
          print("Server has sent pickle msg to client")

        except ssl.SSLError as e:
          print(e)
        except Exception as e:
          print(e)
        finally:
          self.conn.close()
          print("ser_PBB.py waiting for clients' requests ...")


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
