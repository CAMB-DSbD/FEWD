import socket
import ssl

import tqdm
import os

import time
import pickle

def arit(a,b):
    print("arit in files2sockets has beeen called")
    r= a+b
    return r

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

def send_content(content, client_name, sock: socket.socket):
    if isinstance(content, str):
        content_bytes = content.encode()
    else:
        content_bytes = content

    fsize = len(content_bytes)
    progress = tqdm.tqdm(range(fsize), F"ATT responds to {client_name} with encrypted file", unit="B", unit_scale=True, unit_divisor=1024)

    nbytes = 0
    buffer_size = 4096  # Define a buffer size for sending in chunks
    while nbytes < fsize:
        try:
            # Determine the chunk size
            chunk_size = min(buffer_size, fsize - nbytes)
            # Get the chunk from the content
            chunk = content_bytes[nbytes:nbytes + chunk_size]
            # Send the chunk
            sock.send(chunk)
            # Update the progress bar
            progress.update(len(chunk))
            nbytes += len(chunk)
        except ssl.SSLEOFError as e:
            print(f"SSL EOF error occurred: {e}")
            break
        except ssl.SSLError as e:
            print(f"SSL error occurred: {e}")
            break
        except Exception as e:
            print(f"General error occurred: {e}")
            break


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




"""
 Read a serealised message (in pickle format) that 
 contains a list from a socket and return a list.
"""
def recvpicklemsg(clientsocket, headersize, buffer_size):
    # clientsocket: a socket wrapped in SSL context
    #               and already connected to a client
    # headersize:   the size of the header in the msg    
    clisocket= clientsocket
    hsize= headersize

    full_msg = b''
    new_msg = True
    #while True:
    full_msg_rcvd="NO"
    while full_msg_rcvd=="NO":
        print("B4 msg=clisicket.recv ")

        #msg = clisocket.recv(16)
        msg = clisocket.recv(buffer_size)

        print("After msg=clisicket.recv ")
        if new_msg:
            # take the first hsize th elements of the list
            print("new msg len:",msg[:hsize])
            msglen = int(msg[:hsize])
            new_msg = False

        print(f"full message length: {msglen}")

        full_msg += msg

        print(len(full_msg))

        if len(full_msg) - hsize == msglen:
            print("full msg recvd")
            print(full_msg[hsize:])
            print(pickle.loads(full_msg[hsize:]))
            # recover list sent by client
            list=pickle.loads(full_msg[hsize:])
            print("Request from client:")
            for i in range(0, len(list)):
                print("[", i, "]=", list[i])

            new_msg = True
            full_msg = b""
            full_msg_rcvd="YES"
    return list



"""
 Given a list that contains a request (post or
 retrieve) and a socket already connected to a
 client, this function extracts the request,
 composes a response in pickle format with
 consideration of the hsize (header size) and
 sends it back to the client.
 If the request is post s_A or post c_A, the
 function appends the token to the pbbrecrds.
"""
def sendpicklemsg(clisocket, list, hsize, pbbrecrds):
  print("sendpicklemsh has been called")
  if len(list)==2 and list[0] == "post" :
     print("list[0]=", list[0], "list[1]=", list[1])
     # server1 sends response to client
     resplist=[list[1], "has been posted"]
     pbbrecrds.append(list[1])
     msg = pickle.dumps(resplist)
     msg = bytes(f"{len(msg):<{hsize}}", 'utf-8') + msg
     print("This is the msg:::::::::::::::::", msg)
     # server1 sends to client
     clisocket.send(msg)
     print("clisocket has sent msg")

     #clisocket.close()  

  # copy this code to a function
  elif len(list)== 1 and list[0] == "retrieve":
     print("list[0]=", list[0])
     # server1 sends response to client
     msg = pickle.dumps(pbbrecrds)
     msg = bytes(f"{len(msg):<{hsize}}", 'utf-8') + msg
     print(msg)
     # server1 sends to client
     print("B4 clisocket.send(msg)..... ")
     clisocket.send(msg) ############# failing 
     print("After clisocket.send(msg)..... ")
     #clisocket.close()
     print("After clisocket.close..... ")

  # copy this code to a function
  else:
     print("ser: Invalid request received")
     # server1 sends response to client
     resplist = ["Invalid request received"]
     msg = pickle.dumps(resplist)
     msg = bytes(f"{len(msg):<{hsize}}", 'utf-8') + msg
     print(msg)
     # server1 sends to client
     #clisocket.send(msg)


