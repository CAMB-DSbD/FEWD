"""
title           : test_SSLclientfile.py 
description     : It tests the the SSLfileserver class. 
                : By defaut it assumes that the server and the 
                : client are no colocated, that is, that they are
                : on their own computers. 
                : I tested it only on the same LAN, not firewall
                : between server and client.
                :
inspiration     : https://github.com/mikepound/tls-exercises
source          :
                : 
author          : Carlos Molina-Jimenez
                : carlos.molina@cl.cam.ac.uk
                : Computer Lab, University of Cambridge
date            : 8 Sep 2023
version         : 1.0 
                :
usage           : 
notes           :
compile and run :
                : cm770@morello-camb-1: $ py test_SSLclientfile.py 
                :      -s morello-camb-3.sm.cl.cam.ac.uk 
                :      -p 8282 -f helloServer.txt
                : cm770@morello-camb-1: $ py test_SSLclientfile.py 
                :
python_version  : Python 3.7.4 (v3.7.4:e09359112e, Jul 8 2019)      
"""

from cli_send_recv_file import  SSLclientfile 


def main():
  import argparse
  parser = argparse.ArgumentParser(description="Client that that exchanges a file with a server")
  #parser.add_argument("-s", "--server", help="Server, default is localhost", default= "localhost")
  parser.add_argument("-s", "--server", help="Server, default is morello-camb-3.sm.cl.cam.ac.uk", default= "morello-camb-3.sm.cl.cam.ac.uk")
  parser.add_argument("-p", "--port", help="Server port, default is ", default= 8282)
  parser.add_argument("-f", "--file", help="File to send to server, default is helloServer.txt", default= "helloServer.txt")

  args         = parser.parse_args()
  server       = args.server
  port         = args.port  
  file_to_send = args.file
  
  cli= SSLclientfile()
  cli.sockconnect(server, int(port)) # deft server= "morello-camb-3", port=8282
  cli.send_recv_file(file_to_send) 


if __name__ == '__main__':
    main()
