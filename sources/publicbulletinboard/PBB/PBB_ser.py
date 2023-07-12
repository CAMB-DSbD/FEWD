"""
title           : ser_PBB.py 
description     : A server that implements a PBB (Public Bulletin 
                : Board). It can establish a secure chan over ssl
                : with clients and execute requests to post and
                : retrieve tokens. 
                : 
inspiration     : https://github.com/mikepound/tls-exercises
source          :
                : 
author          : Carlos Molina Jimenez
date            : 11 Jul 2023
version         : 1.0 (not complete yet. I have to implement post 
                : and retrieve operations explicitly. 
                : Save to file and sign of responses not
                : implemented yet. 
usage           : 
notes           :
compile and run : % python3 ser_PBB.py 
                : The program expects ca.cert in ../client, that
                : is, in a folder called client located in the
                : parent folder.
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


LOCAL_HOST = 'localhost'
LOCAL_PORT = 8282
RESOURCE_DIRECTORY = Path(__file__).resolve().parent.parent / 'resources' / 'server'
SERVER_CERT_CHAIN = RESOURCE_DIRECTORY / 'server.intermediate.chain.pem'
SERVER_KEY = RESOURCE_DIRECTORY / 'server.key.pem'


# three new lines 
# receive 4096 bytes each time
BUFFER_SIZE = 4096




class SSLServer:
    """
    This is a server
    """
    def __init__(self):
        """
        Creates an SSLContext which provides parameters for any future SSL connections
        """
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=SERVER_CERT_CHAIN, keyfile=SERVER_KEY)

        # You can add code here to disable older protocols and cipher suites. 
        # You can add similar code to the client, too.
        # For help check out:
        #      https://github.com/mikepound/tls-exercises/blob/master/python/README.md

        self.context = context

    def start_server(self):
        """
        Begins listening on a socket. Any connections that arrive are wrapped in 
        an SSLSocket using the context
        created during initialisation

        Makes use of the OS select function to perform basic non-blocking IO. 
        Once a connection has established
        an instance of ClientHandler is created to serve the client
        """

        server_socket = socket.socket()
        server_socket.bind((LOCAL_HOST, LOCAL_PORT))
        server_socket.listen(5)
        read_list = [server_socket]

        print("Listening on port {0}...".format(LOCAL_PORT))

        while True:
            readable, writable, errored = select.select(read_list, [], [], 2)
            for s in readable:
                if s is server_socket:
                    client_socket, address = server_socket.accept()
                    try:
                        # Wrap the socket in an SSL connection (will perform a handshake)
                        conn = self.context.wrap_socket(client_socket, server_side=True)
                        ClientHandler(conn).start()
                        #server_socket.close()   # close the server socket or hang
                    except ssl.SSLError as e:
                        print(e)


class ClientHandler(threading.Thread):
    """
    Thread handler leaves the main thread free to handle any other incoming connections
    """
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        try:
            # Read up to 4x1024 bytes from the client
            ser_str= self.conn.recv(BUFFER_SIZE)
            l=pickle.loads(ser_str)
            for x in range(len(l)):
                print (l[x])
            
            print("ser_PBB.py will now send a string to cliA_str.py")
            lst=["s_A","s_B"]
            ser_string= pickle.dumps(lst)
            
            self.conn.sendall(ser_string)
            print("ser_PBB.py has sent a string to cliA_str.py")

        except ssl.SSLError as e:
            print(e)
        except Exception as e:
            print(e)
        finally:
            self.conn.close()
            print("ser_PBB.py waiting for requests ...")


def main():
    server = SSLServer()
    server.start_server()


if __name__ == '__main__':
    main()
