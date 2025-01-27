"""
title           : ser_send_recv_file.py
description     : Is a server that establishes a secure chan over ssl
                : with a client if mutual authentication succeeds.
                :
                : I created the self-signed certificates following the steps
                : https://github.com/mikepound/tls-exercises/tree/master/ca
                :
                : 1) It listen for a connection request from a 
                :    client.
                : 2) Accepts the request and receives a file.
                : 3) It sends another file as a response.
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
date            : 3 Sep 2023
version         : __
usage           : 
notes           :
compile and run :  cm770@morello-camb-3: $ python3 ser_send_recv_file.py 
                :           -s morello-camb-3.sm.cl.cam.ac.uk 
                :           -f helloClient.txt 
                :
                :  cm770@morello-camb-3: $ python3 ser_send_recv_file.py 
                :
                : Optionally the test_SSLfileserver.py testing
                : program can be used to test the main class:
                : SSLfileserver
                :
                :
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


#LOCAL_HOST = 'localhost'
SERVER_NAME = "morello-camb-3.sm.cl.cam.ac.uk" 
LOCAL_PORT = 8282
RESOURCE_DIRECTORY = Path(__file__).resolve().parent.parent / 'certskeys' / 'server'
SERVER_CERT_CHAIN = RESOURCE_DIRECTORY / 'bobServer.intermediate.chain.pem'
SERVER_KEY = RESOURCE_DIRECTORY / 'bobServer.key.pem'


# three new lines 
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
RECV_FILE_NAME_PREFIX= "fuchi_fromCli_"


class SSLserverfile():
    """
    This is a server
    """
    def __init__(self):
        """
        Creates an SSLContext which provides parameters for any future SSL connections
        """
        print("\nBob's server running... Its PEM pass phrase is: camb\n")
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=SERVER_CERT_CHAIN, keyfile=SERVER_KEY)


        self.context = context
        self.server_name= SERVER_NAME
        self.local_port= LOCAL_PORT

    # Carlos (8 sep 2023): I need to improve this code take the
    # default arguments without duplications
    # Pending task!
    # 
    def start_server(self, server_Name, port_Number, ser_fileName):
        """
        Begins listening on a socket. Any connections that arrive are wrapped in 
        an SSLSocket using the context
        created during initialisation

        Makes use of the OS select function to perform basic non-blocking IO. 
        Once a connection has established
        an instance of ClientHandler is created to serve the client
        """
        self.server_name= server_Name 
        self.local_port= port_Number 

        server_socket = socket.socket()

        server_socket.bind((self.server_name, self.local_port))
        server_socket.listen(5)
        rd_list = [server_socket] # include server_socket to list
        wr_list= []               # empty list
        er_list= []               # empty list

        print("Bob's sever has been started on host: ", self.server_name)
        print("it is listening on port {0}...".format(self.local_port))

        server_socket_open="YES"
        while server_socket_open=="YES":
          readable, writable, errored = select.select(rd_list, wr_list, er_list)
          for s in readable:
            if s is server_socket:
               client_socket, address = server_socket.accept()
               try:
                   # Wrap the socket in an SSL connection (will perform a handshake)
                   conn = self.context.wrap_socket(client_socket, server_side=True)
                   ClientHandler(conn, ser_fileName).start()
                   server_socket.close()   # close the server socket or hang
                   server_socket_open="NO" # close and loop again: produces
               except ssl.SSLError as e:   # ValueError: f descriptor negative
                   print(e)


class ClientHandler(threading.Thread):
    """
    Thread handler leaves the main thread free to 
    handle any other incoming connections
    """
    def __init__(self, conn, ser_fileName):
        threading.Thread.__init__(self)
        self.conn = conn
        self.ser_fileName= ser_fileName
        print("\n\n\n...........ser_fileName:", self.ser_fileName)

    def run(self):
        try:
            # Read up to 1024 bytes from the client
            ###client_req = self.conn.recv(1024)
            ###print("Rcvd from cli_str.py ", client_req.decode("UTF-8").rstrip())
            received= self.conn.recv(BUFFER_SIZE).decode()
            filename, filesize= received.split(SEPARATOR)
            
            # remove filename path if any
            filename= os.path.basename(filename)
            filename= RECV_FILE_NAME_PREFIX + filename
            filesize= int(filesize)
            # start receiving the file from the socket
            # and writing to the file stream
           
            
            ########## server will receive from client ########
            recv_store_file(filename, filesize, BUFFER_SIZE, self.conn)
            print("ser_file_file.py server has read file from socket....")

            
            ########## server will send file to client ########
            # experimenting with marco.txt file stored on current subdir
            filename= self.ser_fileName
            filesize= os.path.getsize(filename)
            # In python sockets send and receive strings. Send a string
            self.conn.send(f"{filename}{SEPARATOR}{filesize}".encode())
            read_send_file(filename, filesize,  BUFFER_SIZE, self.conn)
            print("ser_file_file.py has sent a file to cli_file)flie.py")

            #print("ser_str.py will now send a string to cli_str.py")
            # You are responsible for converting any data into bytes strings
            #self.conn.send(b"2nd: I'm here cli_str.py\n")

        except ssl.SSLError as e:
            print(e)
        except Exception as e:
            print(e)
        finally:
            self.conn.close()
            print("ser_str.py has closed the socket")


def main(server_name, port_number, file_to_send):
    server = SSLserverfile()
    server.start_server(server_name, port_number, file_to_send) 
           # file_to_send: name of the file that ser sends to cli 
           # as response


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Server that receives and send files")
    parser.add_argument("-s", "--server_name", help="Name of host running the server", default="morello-camb-3.sm.cl.cam.ac.uk")
    parser.add_argument("-p", "--port_number", help="port number used by server", default="8282")
    parser.add_argument("-f", "--file_to_send", help="Name of file to send to client", default="helloClient.txt")

    args = parser.parse_args()
    server_name = args.server_name
    port_number= args.port_number
    file_to_send = args.file_to_send

    print("server name is: ", server_name, "port number is:", port_number)
    main(server_name, int(port_number), file_to_send)
