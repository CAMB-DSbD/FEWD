import hashlib
import socket

def start_client(client_name, key, options):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 12345
    client_socket.connect((host, port))

    key_bytes = key.encode('utf-8')
    hash_object = hashlib.sha256(key_bytes)
    hex_dig = hash_object.hexdigest()

    for option in options:
        message = f'{client_name},{hex_dig},{option}'
        print(f"\n{client_name} sent: {option} to PBB")
        client_socket.send(message.encode())

        try:
            response = client_socket.recv(1024).decode()
            if "cancel" in response.lower():
                acao = "Abort exchange."
            else:
                acao = "The exchange can be successfully."
                print(f"{client_name} received the item from the other client.")

            print(f"The PBB responded with: {response}. {acao}")
        except socket.timeout:
            print('Timeout occurred, the message will be removed...')
            remove_message = f'{client_name},{hex_dig},remove'
            client_socket.send(remove_message.encode())
        except ConnectionResetError:
            print('Connection was reset by the server.')
            break

    client_socket.close()

if __name__ == "__main__":
    start_client("alice", "key123", ["Message1"])