"""
title           : cliA_PBB.py 
description     : A client that establishes a secure chan over ssl
                : with a server playing the role of a PBB
                : (Public Bulletin Board) to post and retrieve
                : tokens
                : 
source          : https://github.com/mikepound/tls-exercises
                : 
author          : Carlos Molina Jimenez
date            : 11 Jul 2023
version         : 1.0 (not complete yet. I have to implement post 
                : and retrieve operations explicitly. 
usage           : 
notes           :
compile and run : % python3 cliA_PBB.py 
                : The program expects ca.cert in ../client, that
                : is, in a folder called client located in the
                : parent folder.
python_version  : Python 3.7.4 (v3.7.4:e09359112e, Jul 8 2019)    
                :
"""
import socket
import ssl
from pathlib import Path

# five new lines
import tqdm
import os
import argparse
import pickle

LOCAL_HOST = 'localhost'
LOCAL_PORT = 8282
RESOURCE_DIRECTORY = Path(__file__).resolve().parent.parent / 'resources' / 'client'
CA_CERT = RESOURCE_DIRECTORY / 'ca.cert.pem'


BUFFER_SIZE = 1024 * 4 #4KB


def main():
    """
    This is a client
    """

    # The code here create and configure an SSLContext, wrap a socket 
    # and connect using TLS
    # For help check out:
    #      https://github.com/mikepound/tls-exercises/blob/master/python/README.md

    # Create a standard TCP Socket
    sock= socket.socket(socket.AF_INET)
 

    # Create SSL context which holds the parameters for any sessions
    context= ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname= False
    context.load_verify_locations(CA_CERT)
 

    # We can wrap in an SSL context first, then connect
    conn= context.wrap_socket(sock, server_hostname="Expert TLS Server")
    try:
        # Connect using conn

        # The code below is complete, it will use a connection to send and receive from the server

        conn.connect((LOCAL_HOST,LOCAL_PORT)) 

        # What parameters were established?
        print("Negotiated session using cipher suite: {0}\n".format(conn.cipher()[0]))

        cli_l=["c_A"]
        cli_s=pickle.dumps(cli_l)
        conn.sendall(cli_s)

        print("cliA_str.py now waiting from string from ser_PBB.py")
        # Receive a string back from the server
        ser_resp = conn.recv(BUFFER_SIZE)

        l=pickle.loads(ser_resp)
        for x in range(len(l)):
            print("token[",x,"]=",l[x])

    finally:
      if conn is not None:
         conn.close()


if __name__ == '__main__':
    main()
