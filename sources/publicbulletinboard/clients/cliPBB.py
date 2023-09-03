"""
title           : cliPBB.py
description     : A client (Alice's) that sends a connection request
                : to a server, upon acceptance, the client sends
                : a request: either post s_A or retrieve.
                :
                : I created the self-signed certificates following the steps
                : https://github.com/mikepound/tls-exercises/tree/master/ca
                :
source          : https://pythonprogramming.net/pickle-objects-
                : sockets-tutorial-python-3/ 
                : 
author          : Carlos Molina-Jimenez,
                : carlos.molina@cl.cam.ac.uk
date            : 3 Sep 2023, Computer Lab, University of Cambridge
version         : __ 
usage           : 
notes           :
compile and run : % python3 serPBB.py             on a window shell
                : % python3 cliPBB.py  on another window shell
                :
                : % python3 cliPBB.py -r post -t s_A
                : % python3 cliPBB.py -r retrieve
                :
python_version  : Python 3.7.4(v3.7.4:e09359112e, Jul 8 2019, 14:36:03) 
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

LOCAL_HOST = "localhost"
LOCAL_PORT = 8282
RESOURCE_DIRECTORY = Path(__file__).resolve().parent / 'certskeys' / 'client'
CA_CERT = RESOURCE_DIRECTORY / 'rootca.cert.pem'


BUFFER_SIZE = 1024 * 4 #4KB
HEADERSIZE = 10 


class ClientPBB():

 def __init__(self, clientname= "cliAlice", server=LOCAL_HOST, port=LOCAL_PORT):
  self.clientname= clientname
  self.server= server 
  self.port= port
  self.headersize= HEADERSIZE 
  self.soc= None
  self.conn= None
  print(self.clientname, " has been created!")

 def sockconnect(self, ser="localhost", port=8282):
     self.server= ser
     self.port= port

     self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

     # Create a standard TCP Socket
     # Create SSL context which holds the parameters for any sessions
     context= ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
     context.check_hostname= False
     context.load_verify_locations(CA_CERT)

     # We can wrap in an SSL context first, then connect
     #self.conn= context.wrap_socket(self.soc, server_hostname="Expert TLS Server")
     self.conn= context.wrap_socket(self.soc, server_hostname="PBB server CAMB")

     ## OK 27Jul2023 return(self.conn.connect((ser, port)))
     return(self.conn.connect((self.server, self.port)))
     # this version does not use this return value

 def post(self, token, hsize=HEADERSIZE):
     sockconn= self.conn
     tkn= token 
     self.headersize= hsize 
     hdsize= hsize

     list = ["post", tkn]
     msg = pickle.dumps(list)
     msg = bytes(f"{len(msg):<{hdsize}}", 'utf-8') + msg
     print(msg)
     # server sends to client
     sockconn.send(msg)

     full_msg = b''
     new_msg = True
     full_msg_rcvd="NO"
     while full_msg_rcvd=="NO":
         print("post: Client waiting for new msg from server...")
         #msg = sockconn.recv(16) works fine 27 Jul 2023
         msg = sockconn.recv(BUFFER_SIZE)
         if new_msg:
             # take the first hdsieze_th elements of the list
             print("new msg len:",msg[:hdsize])
             msglen = int(msg[:hdsize])
             new_msg = False

         print(f"full message length: {msglen}")

         full_msg += msg

         print(len(full_msg))

         if len(full_msg)-hdsize == msglen:
             print("Full msg recvd")
             print(full_msg[hdsize:])
             print(pickle.loads(full_msg[hdsize:]))
             list=pickle.loads(full_msg[hdsize:])
             print("Msg received from server: ")
             for i in range(0, len(list)):
                 print("[", i, "]=", list[i])
             new_msg = True
             full_msg = b""
             full_msg_rcvd="YES"
     #s.close()



 def retrieve(self, hsize=HEADERSIZE):
     sockconn= self.conn
     self.headersize= hsize 
     hdsize= hsize

     list = ["retrieve"]
     msg = pickle.dumps(list)
     msg = bytes(f"{len(msg):<{hdsize}}", 'utf-8') + msg
     print(msg)
     # server sends to client
     sockconn.send(msg)
     print("retrieve: Client has sent retrieve to server...")

     full_msg = b''
     new_msg = True
     full_msg_rcvd="NO"
     while full_msg_rcvd=="NO":
         print("retrieve: Client waiting for new msg from server...")
         #msg = sockconn.recv(16) works fine 27Jul2023
         msg = sockconn.recv(BUFFER_SIZE)
         if new_msg:
             # take the first hdsieze_th elements of the list
             print("new msg len:",msg[:hdsize])
             msglen = int(msg[:hdsize])
             new_msg = False

         print(f"full message length: {msglen}")

         full_msg += msg

         print(len(full_msg))

         if len(full_msg)-hdsize == msglen:
             print("Full msg recvd")
             print(full_msg[hdsize:])
             print(pickle.loads(full_msg[hdsize:]))
             list=pickle.loads(full_msg[hdsize:])
             print("Msg received from server: ")
             for i in range(0, len(list)):
                 print("[", i, "]=", list[i])
             new_msg = True
             full_msg = b""
             full_msg_rcvd="YES"
     #s.close()





def main():
   import argparse
   parser = argparse.ArgumentParser(description="A client to PBB with no sec chan")
   parser.add_argument("-c", "--clientname", help="Client to interact with PBB, default is ", default= "cliAlice")
   parser.add_argument("-s", "--server", help="Server implementing the PBB, default is local host", default= "localhost")
   parser.add_argument("-p", "--port", help="Port to use, default is 1243", default=1243)
   parser.add_argument("-r", "--request", help="Request to send, either post or retrieve, default is retrieve", default="retrieve")
   parser.add_argument("-t", "--token", help="Token to post", default="c_A")

   args = parser.parse_args()
   clientname  = args.clientname
   server      = args.server
   port        = args.port
   request     = args.request
   token       = args.token

   c=ClientPBB(clientname, server, int(port))
   sockconnected= c.sockconnect()

   if request == "post":
      c.post(token, 10)  
   elif request == "retrieve":
      c.retrieve()  
   else:
      print("Error: in PBB call parameters")
   #sockconnected.close()


if __name__ == "__main__":
     main()
      
