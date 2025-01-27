import socket
import threading

def handle_client(conn, addr):
    print(f"Bob: Conectado por {addr}")
    C = None  # Inicializa C como None
    buffer = ""  # Buffer para armazenar dados recebidos
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                print("Bob: Conexão fechada pelo cliente.")
                break
            buffer += data
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                line = line.strip()
                if not line:
                    continue
                if line.startswith("C:"):
                    try:
                        C = int(line.split(":")[1])
                        print(f"Bob: Recebido valor inicial C={C}")
                    except ValueError:
                        print("Bob: Valor de C inválido.")
                        conn.sendall("ERROR: Valor de C inválido.\n".encode())
                        continue
                elif line == "MSG_FROM_Alice":
                    if C is None:
                        print("Bob: C ainda não foi definido.")
                        conn.sendall("ERROR: C não foi definido.\n".encode())
                        continue
                    if C > 0:
                        print("Bob: Recebida mensagem de Alice, enviando resposta...")
                        conn.sendall("MSG_FROM_GB\n".encode())
                    else:
                        print("Bob: C já é 0, sincronização concluída.")
                        conn.sendall("SYNC_COMPLETE\n".encode())
                elif line == "SYNC_COMPLETE":
                    print("Bob: Sincronização finalizada com sucesso.")
                    return
                else:
                    print(f"Bob: Mensagem desconhecida: {line}")
                    conn.sendall("ERROR: Mensagem desconhecida.\n".encode())
    except ConnectionResetError:
        print("Bob: Conexão resetada pelo cliente.")
    finally:
        conn.close()
        print(f"Bob: Desconectado de {addr}")

def start_server(host='localhost', port=65445):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Bob: Servidor escutando em {host}:{port}")
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    start_server()
