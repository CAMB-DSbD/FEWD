import threading
import time

from srcFewd.alice.Configurations import ConfigsAlice
from srcFewd.bob.Configurations import ConfigsBob
from srcFewd.client.Client import ClientSSL
from srcFewd.server.ServerSSL import ServerSSL


class ExchangeEncryptedFile():
    def __int__(self):
        pass

    def startProcess(self, conf1, conf2, encrypted_file_Alice, encrypted_file_Bob):

        try:
            print(f"-----------------------------------------------------------------------------------------")
            print(f"------Begin process exchange document-----")
            # Start the server in a new thread
            server_thread = threading.Thread(target=self.upServerToReceivDocEncrypted,
                                             name="exchange_server",
                                             args=(conf1,
                                                   encrypted_file_Bob))
            server_thread.start()

            #client_name = conf1.configuration.client_name + " Server CAMB",
            client_name = "GCA"

            self.upClienteToSendDocumentEncripted(conf2, client_name, encrypted_file_Alice)

            print(f"-----------------------------------------------------------------------------------------")
            print(f"------finish process exchange document-----")
            return True

        except Exception as e:
            print(f"An error occurred during the encryption process: {e}")
            return False, None



    def upServerToReceivDocEncrypted(self, conf,  file_to_exchange):

        server_cert_chain = conf.configuration.config_server.intermadiate_server_cert_chain
        server_key = conf.configuration.config_server.intermadiate_server_key
        host = conf.configuration.server_name
        local_port = 8290
        print(f"------Up {conf.configuration.client_name}'s module to exchange documents-----")
        server = ServerSSL(conf, server_cert_chain, server_key, "exchangeEncryptedFiles", host, local_port, file_to_exchange,True)

    def upClienteToSendDocumentEncripted(self, conf, client_name, file_to_exchange):

        serverName = client_name
        client_cert_chain = conf.configuration.config_client.intermadiate_client_cert_chain
        client_key = conf.configuration.config_client.intermadiate_client_key
        host = conf.configuration.server_name
        port = 8290
        print(f"------Up {conf.configuration.client_name}'s module to exchange documents-----")
        ssl_client_file = ClientSSL(conf, client_cert_chain, client_key, host, port, True)
        ssl_client_file.sock_connect(serverName)
        ssl_client_file.exchange_encrypted_file(file_to_exchange)
        ssl_client_file.conn.close()
