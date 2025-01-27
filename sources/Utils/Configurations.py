import argparse
from pathlib import Path

class Configuration:
  def __init__(self, server_name, local_port, client_name, path_file, separator, buffer_size,  headersize, recv_file_name_prefix,  config_server, config_client ):

    self.server_name = server_name
    self.local_port = local_port
    self.client_name = client_name
    self.path_file = path_file

    self.separator = separator
    self.buffer_size = buffer_size
    self.headersize = headersize
    self.recv_file_name_prefix= recv_file_name_prefix

    self.config_server = config_server
    self.config_client = config_client
