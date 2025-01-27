import hashlib
import socket

import hashlib
import socket

def start_client(client_name, key, option):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 12345
    client_socket.connect((host, port))

    key_bytes = key.encode('utf-8')
    hash_object = hashlib.sha256(key_bytes)
    hex_dig = hash_object.hexdigest()

    message = f'{client_name},{hex_dig},{option}'
    print(f"\n{client_name} sent: {option} to PBB\n")
    client_socket.send(message.encode())

    try:
        responseAction = None
        response = client_socket.recv(1024).decode()
        if "cancel" in response.lower():
            acao = "Abort exchange. \n"+client_name+"'s attestable sends notification of abort to your application"
        else:
            acao = "The exchange can be successfully. \n"+client_name+"'s attestable sends notification of success to your application.\n"+client_name+" received the item from the other client. "
        print(f"The PBB responded with: {response}. {acao}")
    except ConnectionResetError:
        print(f"Connection reset by peer while receiving response for {option}")
    except socket.timeout:
        print('Timeout occurred, the message will be removed...')
        remove_message = f'{client_name},{hex_dig},remove'
        client_socket.send(remove_message.encode())

    return client_socket, responseAction

if __name__ == "__main__":
    start_client("ClientName", "key123", "Message1")