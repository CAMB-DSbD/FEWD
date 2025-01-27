import hashlib
import socket

def start_client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set a timeout of 5 seconds
    #client_socket.settimeout(30)

    # Get local machine name
    host = socket.gethostname()

    # Choose the same port as the server
    port = 12345

    # Connect to the server
    client_socket.connect((host, port))

    # Send a message to the serverF
    client_name = "Alice"  # or "Client2" for client_2.py
    hash_object = hashlib.sha256(b'123')
    hex_dig = hash_object.hexdigest()
    message = f'{client_name},{hex_dig},Sync_A'  # or 'negative' for client_2.py
    print(f" {client_name} sent: Sync_A to PBB")
    client_socket.send(message.encode())


    # Wait for the response from the server
    try:
        while True:
            response = client_socket.recv(1024)
            response = response.decode()
            #if response == 'Sync':
            if "cancel" in response.lower():
                acao = "Abort exchange."
            else:
                acao = "The exchange can be successfully."
            print(f"The PBB responded with: {response}. {acao}")
            print(f"\n {client_name}'s attestable sends notification of abort to your application")
            break
            #else:
            #    print(f"The PBB responded with: {response}_A/Sync_B. The exchange has been aborted")
            #    break
    except socket.timeout:
        print('Timeout occurred, the message will be removed...')
        remove_message = f'{client_name},{hex_dig},remove'
        client_socket.send(remove_message.encode())

    # Close the connection with the server
    client_socket.close()

if __name__ == "__main__":
    start_client()