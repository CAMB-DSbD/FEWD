"""
title           : socket_files.py
description     : This module implements function that perform operations
                : to send and receive files over sockets. 
                :
source          : It is based on the example from
                :  https://www.thepythoncode.com/code/send-receive-files-using-sockets-python 
                :
author          : Carlos Molina Jimenez (Carlos.Molina@cl.cam.ac.uk)
institution     : Computer Lab, University of Cambridge
date            : 3 Jul 2023
version         : 1.0
usage           : 
notes           :
compile and run :  It can be imported by  clients and servers that  send and
                :  receive files over sockets.
                :
python_version  : Python 3.7.4 (default, Oct  8 2019, 14:48:17) 
"""


import socket
import tqdm
import os

"""
Open the file under the given name, read it and send it over
the given socket. 
"""
def read_send_file(fname: str, fsize: int, buffer_size: int, sock: socket):

    progress = tqdm.tqdm(range(fsize), f"Sending {fname}", 
               unit="B", unit_scale=True, unit_divisor=1024)

    with open(fname, "rb") as f:
      nbytes= 0
      while nbytes < fsize:
          # read the bytes from the file
          bytes_read = f.read(buffer_size)
          if not bytes_read:
              # file transmitting is done
              break
          # we use sendall to assure transimission in
          # busy networks
          sock.sendall(bytes_read)
          # update the progress bar
          progress.update(len(bytes_read))
          nbytes= nbytes + len(bytes_read)



"""
Receive a file from a socket and store it on disk under
the give name. 
"""
def recv_store_file(fname: str, fsize: int, buffer_size: int, sock: socket):

    progress = tqdm.tqdm(range(fsize), f"Receiving {fname}", 
               unit="B", unit_scale=True, unit_divisor=1024)
    nbytes= 0
    with open(fname, "wb") as f:
     while nbytes < fsize :
       # read 1024 bytes from the socket 
       bytes_read = sock.recv(buffer_size)
       if not bytes_read:
           # nothing is received
           # file transmitting is done
           break
       # write to the file the bytes we just received
       f.write(bytes_read)
       # update the progress bar
       progress.update(len(bytes_read))
       nbytes= nbytes + len(bytes_read)

