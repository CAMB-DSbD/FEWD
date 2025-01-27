import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from srcFewd.alice.Configurations import ConfigsAlice
from srcFewd.service.SincronizationProcessService import SincronizationProcessService
from srcFewd.service.EncryptationProcessService import EncryptationProcessService
from srcFewd.service.ExchangeEncyptedFileService import ExchangeEncryptedFile
from srcFewd.bob.Configurations import ConfigsBob

def main():
    options = {
        1: start_encryption_process,
        2: start_exchange_process,
        3: select_sincronization_process,
        0: exit_program
    }
    last_successful_option = 0
    encrypted_files_1 = None
    encrypted_files_2 = None

    while True:
        time.sleep(2)
        print_options()
        option = int(input("Enter an option: "))
        if option in options:
            if option > last_successful_option + 1:
                print(f"----------------------------------------------------------------------------------------------------")
                print(f"You must successfully complete option {last_successful_option + 1} before selecting option {option}.")
                print(f"----------------------------------------------------------------------------------------------------")
            else:
                if option == 1:
                    success, encrypted_files_1, encrypted_files_2 = options[option]()
                elif option == 2 and encrypted_files_1 and encrypted_files_2 is not None:
                    success = options[option](encrypted_files_1, encrypted_files_2)
                else:
                    success = options[option]()
                if success:
                    last_successful_option = option
        else:
            print("Invalid option. Please try again.")

def start_encryption_process():
    confAlice, confBob = create_configs()
    successAlice, encrypted_file_Alice  = EncryptationProcessService().startProcess(confAlice)
    successBob, encrypted_file_Bob = EncryptationProcessService().startProcess(confBob)
    return successAlice and successBob, encrypted_file_Alice, encrypted_file_Bob

def start_exchange_process(encrypted_file_Alice, encrypted_file_Bob):
    aliceConf, bobConf = create_configs()
    exchangeDocuments = ExchangeEncryptedFile()
    successExchange = exchangeDocuments.startProcess( aliceConf, bobConf,encrypted_file_Alice, encrypted_file_Bob)
    return successExchange

def select_sincronization_process():
    SincronizationProcessService().display_sync_menu()

def create_configs():
    return ConfigsAlice(), ConfigsBob()

def print_options():
    print("Press 1 to encrypts your document on Attestable.")
    print("Press 2 to exchange documents Encrypted.")
    print("Press 3 select a procotol to sincronization.")
    print("Press 0 to exit of system.")

def open_notepad():
    os.system("start notepad")

def exit_program():
    sys.exit()

if __name__ == '__main__':
    main()