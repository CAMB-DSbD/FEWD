import socket
import os

def load_messages(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
    messages = {}
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) != 3:
            print(f"Invalid line format: {line.strip()}")
            continue
        client_name, client_hash, message = parts
        if client_name not in messages:
            messages[client_name] = {}
        if client_hash not in messages[client_name]:
            messages[client_name][client_hash] = set()
        messages[client_name][client_hash].add(message)
    return messages

def save_message(file_path, client_name, client_hash, message):
    with open(file_path, 'a') as file:
        file.write(f"{client_name},{client_hash},{message}\n")

def start_server():
    host = socket.gethostname()
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    client_messages = {}
    client_sockets = {}
    sent_messages_file = 'sent_messages.txt'
    sent_messages = load_messages(sent_messages_file)

    while True:
        client_socket, addr = server_socket.accept()
        print("Got a connection from %s" % str(addr))
        try:
            data = client_socket.recv(1024)
            client_name, client_hash, message = data.decode().split(',')

            print(f"The PBB Received the {message} message from {client_name} with token {client_hash}")

            if client_name not in sent_messages:
                sent_messages[client_name] = {}
            if client_hash not in sent_messages[client_name]:
                sent_messages[client_name][client_hash] = set()
            sent_messages[client_name][client_hash].add(message)
            save_message(sent_messages_file, client_name, client_hash, message)

            # Check if there are more than 2 messages with the same hash
            all_messages_with_hash = [msg for msgs in sent_messages.values() for hash_msgs in msgs.values() for msg in hash_msgs if client_hash in msgs]
            if len(all_messages_with_hash) > 2:
                result = ', '.join(all_messages_with_hash)
                client_socket.send(result.encode())
                client_socket.close()
                continue

            if client_hash in client_messages:
                result = process_messages([client_messages[client_hash], (client_name, client_hash, message)])
                for socketIt in [client_sockets[client_hash], client_socket]:
                    socketIt.send(result.encode())
                    socketIt.close()
                del client_messages[client_hash]
                del client_sockets[client_hash]
            else:
                client_messages[client_hash] = (client_name, client_hash, message)
                client_sockets[client_hash] = client_socket
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            client_socket.close()

    return server_socket

def process_messages(messages):
    result = ', '.join([f" {message[2]}" for message in messages])
    return result

if __name__ == "__main__":
    start_server()