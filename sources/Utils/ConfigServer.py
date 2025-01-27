import argparse
from pathlib import Path

class ConfigServerModule:
  def __init__(self, resource_directory, server_cert_chain, server_key, intermadiate_server_cert_chain,  intermadiate_server_key,  parser_server, server_file):

    self.resource_directory = resource_directory
    self.server_cert_chain = server_cert_chain
    self.server_key = server_key
    self.intermadiate_server_cert_chain = intermadiate_server_cert_chain
    self.intermadiate_server_key = intermadiate_server_key
    self.parser_server = parser_server
    self.server_file = server_file
