"""
title           : test_ServerPBB.py 
description     : It tests the SeverPBB class. 
                : The name of the server in its certificate is
                : "PBB server CAMB" 
                : 
inspiration     : https://github.com/mikepound/tls-exercises
source          :
                : 
author          : Carlos Molina-Jimenez
                : carlos.molina@cl.cam.ac.uk
                : Computer Lab, University of Cambridge
date            : 9 Sep 2023
version         : 1.0 
                :
usage           : 
notes           :
compile and run :
                : cm770@morello-camb-2: python test_ServerPBB.py
                : Enter PEM pass phrase:
                : PBB Server listening on port 8285...
                : PBB Server operating with openssl version:  OpenSSL 
                : 1.1.1m-freebsd  14 Dec 2021
                :
                : cm770@morello-camb-2: python test_ServerPBB.py 
                :    -s morello-camb-2.sm.cl.cam.ac.uk -p 8285
                : Enter PEM pass phrase:
                : PBB Server listening on port 8285...
                : PBB Server operating with openssl version:  OpenSSL 
                : 1.1.1m-freebsd  14 Dec 2021
                :
python_version  : Python 3.7.4 (v3.7.4:e09359112e, Jul 8 2019)      
"""


from ServerPBB import ServerPBB 


def main():
   import argparse
   parser = argparse.ArgumentParser(description="A server implementing a PBB with sec chan")
   parser.add_argument("-s", "--server", help="Server implementing the PBB, default is morello-camb-2.sm.cl.cam.ac.uk", default= "morello-camb-2.sm.cl.cam.ac.uk")
   parser.add_argument("-p", "--port", help="Port to use, default is 8285", default=8285)

   args    = parser.parse_args()
   server  = args.server
   port    = args.port

   pbbser = ServerPBB(server, int(port))
   pbbser.start_server()

if __name__ == '__main__':
    main()
