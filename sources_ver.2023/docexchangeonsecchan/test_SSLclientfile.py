"""
title           : test_SSLclientfile.py 
description     : It tests the the SSLfileserver class. 
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
compile and run : % python3 test_SSLclientfile.py -f file2send
                :
                : % python3 py test_SSLclientfile.py -s "localhost" -p 8282 -f file2send
                :
python_version  : Python 3.7.4 (v3.7.4:e09359112e, Jul 8 2019)      
"""

from cli_send_recv_file import  SSLclientfile 


def main():
  import argparse
  parser = argparse.ArgumentParser(description="Server that receives and send files")
  parser.add_argument("-s", "--server", help="Server, default is localhost", default= "localhost")
  parser.add_argument("-p", "--port", help="Server port, default is ", default=8282)
  parser.add_argument("-f", "--file", help="Name of file to send to server", default= "helloServer.txt")

  args         = parser.parse_args()
  server       = args.server
  port         = args.port  
  file_to_send = args.file
  
  cli= SSLclientfile()
  cli.sockconnect(server, int(port)) # deft server= "localhost", port=8282
  cli.send_recv_file(file_to_send) 


if __name__ == '__main__':
    main()
