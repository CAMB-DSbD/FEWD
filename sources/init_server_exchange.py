from srcFewd.alice.Configurations import ConfigsAlice
from srcFewd.service.EncryptationProcessService import EncryptationProcessService
from srcFewd.service.ExchangeEncyptedFileService import ExchangeEncryptedFile


def main():

    confAlice = ConfigsAlice()
    file = confAlice.configuration.path_file / 'alicedoc_encrypted.txt'
    ExchangeEncryptedFile().upServerToReceivDocEncrypted(confAlice, file)
if __name__ == '__main__':
    main()