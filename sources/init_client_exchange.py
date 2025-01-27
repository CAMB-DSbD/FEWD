from srcFewd.alice.Configurations import ConfigsAlice
from srcFewd.bob.Configurations import ConfigsBob
from srcFewd.service.EncryptationProcessService import EncryptationProcessService
from srcFewd.service.ExchangeEncyptedFileService import ExchangeEncryptedFile


def main():

    confBob = ConfigsBob()

    file = confBob.configuration.path_file / 'bobdoc_encrypted.txt'
    client_name = 'GCA'
    ExchangeEncryptedFile().upClienteToSendDocumentEncripted(confBob, client_name, file)

if __name__ == '__main__':
    main()