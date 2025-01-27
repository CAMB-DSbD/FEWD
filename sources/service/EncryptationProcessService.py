import threading
import time

from srcFewd.client.Client import ClientSSL
from srcFewd.server.ServerSSL import ServerSSL


class EncryptationProcessService():
    def __init__(self):
        pass

    def startProcess(self, conf):

        if conf is None:
            return False
        try:
            print(f"-----------------------------------------------------------------------------------------")
            print(f"------Begin process encryption {conf.configuration.client_name}'s document-----")

            server_thread = threading.Thread(target=self.start_server, name="encryption_server", args=(conf,))
            server_thread.start()

            client, received_file = self.start_client(conf)

            print(f"------Finish process encryption {conf.configuration.client_name}'s document-----")
            time.sleep(2)

            return True, received_file
        except Exception as e:
            print(f"An error occurred during the encryption process: {e}")
            return False, None

    def start_server(self, conf):
        server = ServerSSL(conf, conf.configuration.config_server.server_cert_chain,
                  conf.configuration.config_server.server_key,
                  "uploadFile",
                  conf.configuration.server_name,
                  conf.configuration.local_port, None, True)
        print(f" --> 1 - {conf.configuration.client_name} start your Attestable")

        return server

    def start_client(self, conf):
        client = ClientSSL(conf, conf.configuration.config_client.client_cert_chain,
                           conf.configuration.config_client.client_key, conf.configuration.server_name,
                           conf.configuration.local_port, True)

        #client.sock_connect("attestable " + conf.configuration.client_name + " CAMB")
        client.sock_connect("GCA")

        path_f = conf.configuration.path_file
        print(f'path file: {path_f}')
        cliente_f = conf.configuration.config_client.cliente_file
        print(f'client file: {cliente_f}')

        received_file = client.send_and_receive_encrypted_file( path_f / cliente_f)

        print("client request: ", received_file)
        return client, path_f/ received_file
