# file_common.py

import socket
import ssl
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class FileCommon:
    def encrypt_file(self, file_content, key):

        cipher = Cipher(algorithms.AES(key), modes.CFB(b'\0' * 16), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(file_content) + encryptor.finalize()

        return ciphertext

    def decrypt_file(self, ciphertext, key):
        cipher = Cipher(algorithms.AES(key), modes.CFB(b'\0' * 16), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        return plaintext
