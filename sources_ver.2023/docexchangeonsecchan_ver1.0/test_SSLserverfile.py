"""
title           : test_SSLserverfile() 
description     : It tests the the SSLserverfile class. 
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
notes           : I have tested only with "localhost" (i.e 127.0.0.1)
                : and port 8282
compile and run : % python3 test_SSLserverfile.py -f file_to_send
                : Alternatively
                : % python3 test_SSLserverfile.py 
                :   It assumes the existence of helloClient.txt 
                :   in current folder. 
                :
python_version  : Python 3.7.4 (v3.7.4:e09359112e, Jul 8 2019)      
                :
"""

from ser_send_recv_file import  SSLserverfile 


def main():
  import argparse
  parser = argparse.ArgumentParser(description="Server that receives and send files")
  parser.add_argument("-f", "--file_to_send", help="Name of file to send to client", default="helloClient.txt")
  args = parser.parse_args()
  file_to_send = args.file_to_send
  
  server = SSLserverfile()
  server.start_server(file_to_send) #file_to_send: name of the file
                                    # that ser sends to cli as response

if __name__ == '__main__':
    main()
