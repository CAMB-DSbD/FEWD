import ssl

from srcFewd.server.Utils.file_common import FileCommon
from srcFewd.server.Utils.files2sockets import read_send_file, recv_store_file, send_content
import os

class ClientHandler:
  """
  Thread handler leaves the main thread free to
  handle any other incoming connections
  """

  def __init__(self, conn, conf, option):

    self.conn = conn
    self.conf = conf
    self.ser_fileName = self.conf.config_server.server_file
    self.option = option
    print("\n\n\n...........ser_fileName:", self.ser_fileName)

  def start(self):
    if self.option == 'uploadFile':
      self.uptloadFile()
    elif self.option == 'exchangeEncryptedFiles':
      self.exchangeEncryptedFiles()
  def uptloadFile(self):
    try:

      cli_req = self.conn.recv(1024)
      #print("client request: ", cli_req.decode("UTF-8"))

      # In python sockets send and receive strings. Send a string
      key = b"thisisaverysecretkey123"[:32].ljust(32, b'\0')

      file_common = FileCommon()
      encryptedContent = file_common.encrypt_file(cli_req, key)
      send_content(encryptedContent,self.conf.client_name, self.conn)
      print("ser_file_file.py has sent a file to cli_file)flie.py")

      # print("ser_str.py will now send a string to cli_str.py")
      # You are responsible for converting any data into bytes strings
      # self.conn.send(b"2nd: I'm here cli_str.py\n")

    except ssl.SSLError as e:
      print(e)
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
      print("ser_str.py has closed the socket")

  def exchangeEncryptedFiles(self):
    try:
      # Read up to 1024 bytes from the client
      ###client_req = self.conn.recv(1024)
      ###print("Rcvd from cli_str.py ", client_req.decode("UTF-8").rstrip())
      received = self.conn.recv(self.conf.buffer_size).decode()
      buffer_size = self.conf.buffer_size
      filename, filesize = received.split(self.conf.separator)

      # remove filename path if any
      filename = os.path.basename(filename)
      filename = filename
      filesize = int(filesize)
      # start receiving the file from the socket
      # and writing to the file stream

      ########## server will receive from client ########
      recv_store_file(self.conf.path_file/filename, filesize, buffer_size, self.conn)
      print("ser_file_file.py server has read file from socket....")

      ########## server will send file to client ########
      # experimenting with marco.txt file stored on current subdir
      filename = self.ser_fileName
      filesize = os.path.getsize(filename)
      # In python sockets send and receive strings. Send a string
      self.conn.send(f"{filename}{self.conf.separator}{filesize}".encode())
      read_send_file(filename, filesize, buffer_size, self.conn)
      print("ser_file_file.py has sent a file to cli_file)flie.py")

      # print("ser_str.py will now send a string to cli_str.py")
      # You are responsible for converting any data into bytes strings
      # self.conn.send(b"2nd: I'm here cli_str.py\n")

    except ssl.SSLError as e:
      print(e)
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
      print("ser_str.py has closed the socket")