import hashlib
import socket
import threading
import time

from srcFewd.PBB.client import start_client
from srcFewd.PBB.main_pbb import start_server

class PBBService():
    def __init__(self):
        self.server_socket = None

    # def startProcess(self, list_of_options):
    #     print(f"-----------------------------------------------------------------------------------------")
    #     print(f"------Begin PBB process -----")
    #     i = 0
    #     for person in list_of_options:
    #
    #         if i == 0:
    #             server_thread = threading.Thread(target=lambda: setattr(self, 'server_socket', self.startPbbServer()), name="pbb_server")
    #             server_thread.start()
    #             time.sleep(2)
    #
    #
    #         for mensagem in person['value']:
    #
    #             # Criar um thread para cada cliente e enviar as mensagens
    #             client_thread = threading.Thread(target=self.upClienteToSendSignalToPBB, args=(person['cliente_name'], person["pass"], mensagem))
    #             client_thread.start()
    #
    #                 # time.sleep(2)
    #
    #         i += 1
    #
    #     print(f"-----------------------------------------------------------------------------------------")
    #     print(f"------finish PBB process-----")
    #
    #     if self.server_socket:
    #         self.server_socket.close()

    def startPbbServer(self):
        return start_server()

    def upClienteToSendSignalToPBB(self, clientName, key, signal):
        return start_client(clientName, key, signal)

    def syncA_syncB(self):
        server_thread = threading.Thread(target=lambda: setattr(self, 'server_socket', self.startPbbServer()),name="pbb_server")
        server_thread.start()
        time.sleep(2)

        client_thread = threading.Thread(target=self.upClienteToSendSignalToPBB, args=("Alice", "123", "Sync_A"))
        client_thread.start()

        self.client_socket = self.upClienteToSendSignalToPBB("Bob", "123", "Sync_B")


    def syncA_cancelB(self):
        server_thread = threading.Thread(target=lambda: setattr(self, 'server_socket', self.startPbbServer()),name="pbb_server")
        server_thread.start()
        time.sleep(2)

        client_thread = threading.Thread(target=self.upClienteToSendSignalToPBB, args=("Alice", "123", "Sync_A"))
        client_thread.start()

        self.client_socket = self.upClienteToSendSignalToPBB("Bob", "123", "Cancel_B")

    def syncA_cancelA_SyncB(self):
        server_thread = threading.Thread(target=lambda: setattr(self, 'server_socket', self.startPbbServer()),name="pbb_server")
        server_thread.start()
        time.sleep(2)

        client_thread = threading.Thread(target=self.upClienteToSendSignalToPBB,  args=("Alice", "1233", "Sync_A"))
        client_thread.start()
        time.sleep(1)

        client_thread1 = threading.Thread(target=self.upClienteToSendSignalToPBB, args=("Alice", "1233", "Cancel_A"))
        client_thread1.start()
        time.sleep(1)

        self.upClienteToSendSignalToPBB("Bob", "1233", "Sync_B")

    def cancelA_syncB(self):
        server_thread = threading.Thread(target=lambda: setattr(self, 'server_socket', self.startPbbServer()),name="pbb_server")
        server_thread.start()
        time.sleep(2)

        client_thread1 = threading.Thread(target=self.upClienteToSendSignalToPBB,  args=("Alice", "1231", "Cancel_A"))
        client_thread1.start()

        self.upClienteToSendSignalToPBB("Bob", "1231", "Sync_B")

    ############################################################################################################
    def syncB_syncA(self):
        server_thread = threading.Thread(target=lambda: setattr(self, 'server_socket', self.startPbbServer()),
                                         name="pbb_server")
        server_thread.start()
        time.sleep(2)

        client_thread1 = threading.Thread(target=self.upClienteToSendSignalToPBB, args=("Bob", "123", "Sync_B"))
        client_thread1.start()

        self.client_socket = self.upClienteToSendSignalToPBB("Alice", "123", "Sync_A")

    def syncB_cancelA(self):
        server_thread = threading.Thread(target=lambda: setattr(self, 'server_socket', self.startPbbServer()),
                                         name="pbb_server")
        server_thread.start()
        time.sleep(2)

        client_thread = threading.Thread(target=self.upClienteToSendSignalToPBB, args=("Bob", "123", "Sync_B"))
        client_thread.start()

        self.client_socket1 = self.upClienteToSendSignalToPBB("Alice", "123", "Cancel_A")

    def syncB_cancelB_SyncA(self):
        server_thread = threading.Thread(target=lambda: setattr(self, 'server_socket', self.startPbbServer()),
                                         name="pbb_server")
        server_thread.start()
        time.sleep(2)

        client_thread = threading.Thread(target=self.upClienteToSendSignalToPBB, args=("Bob", "1233", "Sync_B"))
        client_thread.start()
        #time.sleep(1)

        client_thread1 = threading.Thread(target=self.upClienteToSendSignalToPBB, args=("Bob", "1233", "Cancel_B"))
        client_thread1.start()
        #time.sleep(1)

        self.upClienteToSendSignalToPBB("Alice", "1233", "Sync_A")
        time.sleep(1)

    def cancelB_syncA(self):
        server_thread = threading.Thread(target=lambda: setattr(self, 'server_socket', self.startPbbServer()),
                                         name="pbb_server")
        server_thread.start()
        time.sleep(2)

        client_thread = threading.Thread(target=self.upClienteToSendSignalToPBB, args=("Bob", "1231", "Cancel_B"))
        client_thread.start()
        time.sleep(2)

        self.upClienteToSendSignalToPBB("Alice", "1231", "Sync_A")

