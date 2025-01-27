from srcFewd.alice.Configurations import ConfigsAlice
from srcFewd.service.EncryptationProcessService import EncryptationProcessService


def main():

    confAlice = ConfigsAlice()
    client, received_file = EncryptationProcessService().start_client(confAlice)
if __name__ == '__main__':
    main()