"""
title           : test_ClientPBB.py 
description     : It tests the  ClientPBB class.  
                : 
inspiration     : https://github.com/mikepound/tls-exercises
source          :
                : 
author          : Carlos Molina-Jimenez
                : carlos.molina@cl.cam.ac.uk, 
                : Computer Lab, Univ. of Cambridge              
date            : 27 Jul 2023
version         : 1.0 
usage           : 
notes           :
compile and run : % python3 test_ServerPBB.py  on a window shell
                : % python3 test_ClientPBB.py  on another window shell
                :
                : % python3 test_ClientPBB.py -c cliAlice -r post -t s_A
                : % python3 ClientPBB.py -c cliAlice -r retrieve
                :
python_version  : Python 3.7.4(v3.7.4:e09359112e, Jul 8 2019, 14:36:03) 
                :
"""

from cliPBB import ClientPBB 


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
   sockconnected= c.sockconnect() # I dont use return value

   if request == "post":
      c.post(token, 10)  
   elif request == "retrieve":
      c.retrieve()  
   else:
      print("Error: in PBB call parameters")
   #sockconnected.close()


if __name__ == "__main__":
     main()
