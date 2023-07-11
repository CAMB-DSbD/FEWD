"""
title           : ser_file_file.py
description     : A server that establishes a secure chan over ssl
                : with a server to send a file and receive another
                : file as response.
                : I tested it with plain txt, jpeg and encrypted
                : files under
                : encrypt
                : $ openssl aes-256-cbc -e -salt -pbkdf2 -iter 10000 -in 
                :   cat.jpg -out cat_encrypted.dat
                : decrypt
                : $ openssl aes-256-cbc -d -salt -pbkdf2 -iter 10000 -in
                : cat_encrypted.dat -out cat_decrypted.jpg
                :
source          : https://github.com/mikepound/tls-exercises
                : 
author          : Carlos Molina Jimenez
date            : 1 Jul 2023
version         : 1.0
usage           : 
notes           :
compile and run : % python3 ser_file_file.py 
python_version  :     
                :

notes           : rcvd is a blocking call
                : https://stackoverflow.com/questions/7174927/
                :         when-does-socket-recvrecv-size-return
"""


import socket
import ssl
import threading
from pathlib import Path
import select

import tqdm
import os

from files2sockets import read_send_file, recv_store_file


LOCAL_HOST = 'localhost'
LOCAL_PORT = 8282
RESOURCE_DIRECTORY = Path(__file__).resolve().parent.parent / 'resources' / 'server'
SERVER_CERT_CHAIN = RESOURCE_DIRECTORY / 'server.intermediate.chain.pem'
SERVER_KEY = RESOURCE_DIRECTORY / 'server.key.pem'


# three new lines 
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
#SER_FILE_NAME= "marco.txt"
SER_FILE_NAME= "catencrypted"
FILE_NAME_PREFIX= "fuchi"


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
        rd_list = [server_socket] # include server_socket to list
        wr_list= []               # empty list
        er_list= []               # empty list

        print("Listening on port {0}...".format(LOCAL_PORT))

        server_socket_open="YES"
        while server_socket_open=="YES":
          readable, writable, errored = select.select(rd_list, wr_list, er_list)
          for s in readable:
            if s is server_socket:
               client_socket, address = server_socket.accept()
               try:
                   # Wrap the socket in an SSL connection (will perform a handshake)
                   conn = self.context.wrap_socket(client_socket, server_side=True)
                   ClientHandler(conn).start()
                   server_socket.close()   # close the server socket or hang
                   server_socket_open="NO" # close and loop again: produces
               except ssl.SSLError as e:   # ValueError: f descriptor negative
                   print(e)


class ClientHandler(threading.Thread):
    """
    Thread handler leaves the main thread free to 
    handle any other incoming connections
    """
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        try:
            # Read up to 1024 bytes from the client
            ###client_req = self.conn.recv(1024)
            ###print("Rcvd from cli_str.py ", client_req.decode("UTF-8").rstrip())
            received= self.conn.recv(BUFFER_SIZE).decode()
            filename, filesize= received.split(SEPARATOR)
            
            # remove filename path if any
            filename= os.path.basename(filename)
            filename= FILE_NAME_PREFIX + filename
            filesize= int(filesize)
            # start receiving the file from the socket
            # and writing to the file stream
           
            
            print("s.py will now read file from socket....")
            recv_store_file(filename, filesize, BUFFER_SIZE, self.conn)

            
            ########## server will send file to client ########
            # experimenting with marco.txt file stored on current subdir
            filename= SER_FILE_NAME
            filesize= os.path.getsize(filename)
            # In python sockets send and receive strings. Send a string
            self.conn.send(f"{filename}{SEPARATOR}{filesize}".encode())
            read_send_file(filename, filesize,  BUFFER_SIZE, self.conn)

            #print("ser_str.py will now send a string to cli_str.py")
            # You are responsible for converting any data into bytes strings
            #self.conn.send(b"2nd: I'm here cli_str.py\n")
            print("ser_str.py has sent a file to cli_str.py")

        except ssl.SSLError as e:
            print(e)
        except Exception as e:
            print(e)
        finally:
            self.conn.close()
            print("ser_str.py has closed the socket")


def main():
    server = SSLServer()
    server.start_server()


if __name__ == '__main__':
    main()
