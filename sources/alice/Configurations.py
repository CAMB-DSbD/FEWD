import argparse
from pathlib import Path
from srcFewd.Utils.Configurations import Configuration
from srcFewd.Utils.ConfigServer import ConfigServerModule
from srcFewd.Utils.ConfigClient import ConfigClientModule

class ConfigsAlice:

  def __init__(self):
    server_name = "localhost"
    local_port = 8290
    client_name = "Alice"
    buffer_size = 4096
    separator = "<SEPARATOR>"
    recv_file_name_prefix = ""
    headersize = 10
    path_file = Path(__file__).resolve().parent / "files"
    server_file = "alicedoc_encrypted.txt"
    cliente_file = "aliceFile.txt"

    #resource_directory = Path(__file__).resolve().parent.parent.parent / 'certskeys' / 'server'
    #server_cert_chain = resource_directory / 'attAlice.intermediate.chain.pem'
    #server_key = resource_directory / 'attAlice.key.pem'
    resource_directory = Path(__file__).resolve().parent.parent.parent / 'certskeys' / 'alice'
    server_cert_chain = resource_directory / 'server.cert.pem'
    server_key = resource_directory / 'server.key.pem'

    #configuracoes para o servidor(modulo - attestable)
    #intermadiate_server_key = resource_directory / 'aliceServer.key.pem'
    #intermadiate_server_cert_chain = resource_directory / 'aliceServer.intermediate.chain.pem'

    intermadiate_server_key = resource_directory / 'server.key.pem'
    intermadiate_server_cert_chain = resource_directory / 'server.intermediate.chain.pem'

    configServerModule = ConfigServerModule( resource_directory, server_cert_chain, server_key, intermadiate_server_cert_chain,  intermadiate_server_key, None, server_file)

    #configuracoes para comunicar com o servidor(modulo - attestable)
#    resource_directory_client = Path(__file__).resolve().parent.parent.parent / 'certskeys' / 'client'
#    client_cert_chain = resource_directory_client / 'aliceClient.intermediate.chain.pem'
#    client_key = resource_directory_client / 'aliceClient.key.pem'

    resource_directory_client = Path(__file__).resolve().parent.parent.parent / 'certskeys' / 'alice'
    client_cert_chain = resource_directory_client / 'client.chain.pem'
    client_key = resource_directory_client / 'client.key.pem'

    #configuracoes para troca dos arquivos entre bob e alice
    #intermadiate_client_cert_chain = resource_directory_client / 'aliceClient.intermediate.chain.pem'
    #intermadiate_client_key = resource_directory_client / 'aliceClient.key.pem'

    intermadiate_client_cert_chain = resource_directory_client / 'client.intermediate.chain.pem'
    intermadiate_client_key = resource_directory_client / 'client.key.pem'

    ca_cert = resource_directory_client / 'rootca.cert.pem'

    configClientModule = ConfigClientModule( resource_directory_client, client_cert_chain, client_key, intermadiate_client_cert_chain, intermadiate_client_key, ca_cert, None, cliente_file)

    self.configuration = Configuration(server_name, local_port, client_name, path_file, separator, buffer_size, headersize, recv_file_name_prefix, configServerModule, configClientModule)
