import socket
import ssl
import os
import time

from tqdm import tqdm

from srcFewd.server.Utils.files2sockets import recv_store_file, read_send_file


class ClientSSL():
    def __init__(self, config_client, client_cert_chain, client_key, host, port, use_ssl=True):
        self.config_client = config_client
        config = config_client.configuration
        self.client_name = config.client_name
        self.client_cert_chain = client_cert_chain
        self.client_key = client_key
        self.server = host
        self.port = port
        self.headersize = config.headersize
        self.soc = None
        self.conn = None
        self.use_ssl = use_ssl



    def sock_connect(self, serverName):
        self.server = self.server
        self.port = self.port

        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.use_ssl:
            # Create a standard TCP Socket
            # Create SSL context which holds the parameters for any sessions
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.load_verify_locations(self.config_client.configuration.config_client.ca_cert)
            context.load_cert_chain(certfile=self.client_cert_chain,
                                    keyfile=self.client_key, password="camb")

            # We can wrap in an SSL context first, then connect
            self.conn = context.wrap_socket(self.soc, server_hostname=serverName)
            #self.conn = context.wrap_socket(self.soc, server_hostname=serverName + " CAMB")
        else:
            self.conn = self.soc
        # OK 27Jul2023
        self.conn.connect((self.server, self.port))

    def send_recv_file(self, filename):
        try:
            # This method uses the already connected conn socket
            print("Negotiated session using cipher suite: {0}\n".format(self.conn.cipher()[0]))

            print("cli-request_file.py: before send")
            self.conn.send(b"Send me your encrypted doc!\n")
            print("cli-request_file.py: after send")

            print("cli_file_flie.py now waiting from string from ser_file_file.py")
            received = self.conn.recv(self.config_client.configuration.buffer_size).decode()
            remote_filename, filesize = received.split(self.config_client.configuration.separator)
            remote_filename = os.path.basename(remote_filename)
            remote_filename = self.config_client.configuration.recv_file_name_prefix + remote_filename
            filesize = int(filesize)
            recv_store_file(remote_filename, filesize, self.config_client.configuration.buffer_size, self.conn)
            print("cli_file_flie.py has received file from ser_file_file.py")

        finally:
            if self.conn is not None:
                self.conn.close()

    def send_and_receive_encrypted_file(self, file_path):
        progress = None
        try:
            # Read the original file data
            with open(file_path, 'rb') as file:
                file_data = file.read()

            file_size = os.path.getsize(file_path)

            progress = tqdm(total=file_size, desc=F"{self.client_name} sends file to ATT for encryption", unit="B", unit_scale=True)

            # send data file to server
            block_size = 1024  # 1KB
            for i in range(0, len(file_data), block_size):
                data_block = file_data[i:i + block_size]
                self.conn.sendall(data_block)
                progress.update(len(data_block))

            # Receive response from server
            response = self.conn.recv(4096)  # Adjust buffer size as needed
            print(f"Response from server")

            # Get the base name of the original file and add "_encrypted" to it
            base_name = os.path.basename(file_path)
            encrypted_file_name = f"{self.client_name}doc_encrypted{os.path.splitext(base_name)[1]}".lower()

            # Write the original file data to a new file in the 'alice/files' directory
            with open(f'{self.client_name}/files/{encrypted_file_name}'.lower(), 'wb') as temp_file:
                temp_file.write(response)
            return encrypted_file_name
        except Exception as e:
            print(f"erro to send file to server: {e}")
        finally:
            if self.conn is not None:
                self.conn.close()
            if progress is not None:
                progress.close()


        # Return the new encrypted file name
    def exchange_encrypted_file(self, filename):
        conn = self.conn
        separator = self.config_client.configuration.separator
        buffer_size = self.config_client.configuration.buffer_size
        try:
            # This method uses the already connected conn socket

            print("Negotiated session using cipher suite: {0}\n".format(conn.cipher()[0]))

            # experimenting with simon.txt file stored on current subdir
            # filename= FILE_NAME
            filesize = os.path.getsize(filename)

            # In python sockets send and receive strings. Send a string
            conn.send(f"{filename}{separator}{filesize}".encode())

            ########## client will send file to server ########
            read_send_file(filename, filesize, buffer_size, conn)

            #####  client will receive file from server #####
            print("cli_file_flie.py now waiting from string from ser_file_file.py")
            received = conn.recv(buffer_size).decode()
            filename, filesize = received.split(separator)
            # remove filename path if any
            filename = os.path.basename(filename)
            filesize = int(filesize)
            # start receiving the file from the socket
            # and writing to the file stream
            recv_store_file(self.config_client.configuration.path_file/filename, filesize, buffer_size, conn)
            print("cli_file_flie.py has received file from ser_file_file.py")

        finally:
            if self.conn is not None:
                self.conn.close()
    def close_socket(self):
        if self.conn is not None:
            self.soc.close()
            self.conn.close()