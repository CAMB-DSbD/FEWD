from srcFewd.alice.Configurations import ConfigsAlice
from srcFewd.service.EncryptationProcessService import EncryptationProcessService


def main():

    confAlice = ConfigsAlice()
    EncryptationProcessService().start_server(confAlice)
if __name__ == '__main__':
    main()