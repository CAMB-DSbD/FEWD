"""
title           : test_ServerPBB.py 
description     : It tests the SeverPBB class. 
                : 
inspiration     : https://github.com/mikepound/tls-exercises
source          :
                : 
author          : Carlos Molina-Jimenez
                : carlos.molina@cl.cam.ac.uk
                : Computer Lab, University of Cambridge
date            : 27 Jul 2023
version         : 1.0 
                :
usage           : 
notes           :
compile and run : % python3 test_ServerPBB.py 
                :
                : % python3 test_ServerPBB.py
                : PBB Server listening on port 8282...
                : 
                : % python3 test_ServerPBB -s localhost -p 8280
                : PBB Server listening on port 8280...
                :
python_version  : Python 3.7.4 (v3.7.4:e09359112e, Jul 8 2019)      
"""


from serPBB import ServerPBB 


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
