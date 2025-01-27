import argparse
from pathlib import Path
from srcFewd.Utils.Configurations import Configuration
from srcFewd.Utils.ConfigServer import ConfigServerModule
from srcFewd.Utils.ConfigClient import ConfigClientModule

class ConfigsBob:

  def __init__(self):
    server_name = "localhost"
    local_port = 8291
    client_name = "Bob"
    buffer_size = 4096
    separator = "<SEPARATOR>"
    recv_file_name_prefix = ""
    headersize = 10
    path_file = Path(__file__).resolve().parent / "files"
    server_file = "bobdoc_encrypted.txt"
    cliente_file = "bobFile.txt"

    #resource_directory = Path(__file__).resolve().parent.parent.parent / 'certskeys' / 'server'
    #server_cert_chain = resource_directory / 'attBob.intermediate.chain.pem'
    #server_key = resource_directory / 'attBob.key.pem'

    resource_directory = Path(__file__).resolve().parent.parent.parent / 'certskeys' / 'bob'
    server_cert_chain = resource_directory / 'server.cert.pem'
    server_key = resource_directory / 'server.key.pem'

    #intermadiate_server_cert_chain = resource_directory / 'bobServer.intermediate.chain.pem'
    #intermadiate_server_key = resource_directory / 'bobServer.key.pem'

    intermadiate_server_cert_chain = resource_directory / 'server.intermediate.chain.pem'
    intermadiate_server_key = resource_directory / 'server.key.pem'


    configServerModule = ConfigServerModule( resource_directory, server_cert_chain, server_key, intermadiate_server_cert_chain,  intermadiate_server_key,  None, server_file)

    #resource_directory_client = Path(__file__).resolve().parent.parent.parent / 'certskeys' / 'client'
    #client_cert_chain = resource_directory_client / 'bobClient.intermediate.chain.pem'
    #client_key = resource_directory_client / 'bobClient.key.pem'

    resource_directory_client = Path(__file__).resolve().parent.parent.parent / 'certskeys' / 'bob'
    client_cert_chain = resource_directory_client / 'client.chain.pem'
    client_key = resource_directory_client / 'client.key.pem'

#    intermadiate_client_cert_chain = resource_directory_client / 'bobClient.intermediate.chain.pem'
#    intermadiate_client_key = resource_directory_client / 'bobClient.key.pem'
#    ca_cert = resource_directory_client / 'rootca.cert.pem'

    intermadiate_client_cert_chain = resource_directory_client / 'client.intermediate.chain.pem'
    intermadiate_client_key = resource_directory_client / 'client.key.pem'
    ca_cert = resource_directory_client / 'rootca.cert.pem'

    configClientModule = ConfigClientModule( resource_directory_client, client_cert_chain, client_key, intermadiate_client_cert_chain, intermadiate_client_key, ca_cert, None, cliente_file)

    self.configuration = Configuration(server_name, local_port, client_name, path_file, separator, buffer_size, headersize, recv_file_name_prefix, configServerModule, configClientModule)
