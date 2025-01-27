import socket
import random
import time

def alice_client(host='localhost', port=65445):
    sync_value = random.randint(5, 10)
    print(f"Alice: Enviando valor C={sync_value} para Bob")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            # Enviar o valor inicial de C
            s.sendall(f"C:{sync_value}\n".encode())

            while sync_value > 0:
                # Enviar uma mensagem para GB e esperar pela resposta
                print("Alice: Enviando mensagem para GB.")
                s.sendall("MSG_FROM_Alice\n".encode())

                # Definir timeout para esperar pela resposta
                s.settimeout(2.0)
                try:
                    data = s.recv(1024).decode().strip()
                    if not data:
                        print("Alice: Conexão fechada por GB.")
                        break

                    if data == "MSG_FROM_Bob":
                        sync_value -= 1
                        print(f"Alice: Recebida mensagem de Bob, decrementando C para {sync_value}")
                        if sync_value == 0:
                            print("Alice: Sincronização concluída com sucesso!")
                            s.sendall("SYNC_COMPLETE\n".encode())
                            break
                    elif data.startswith("ERROR"):
                        print(f"Alice: Erro recebido de GB: {data}")
                        break
                    elif data == "SYNC_COMPLETE":
                        print("Alice: Sincronização finalizada com sucesso!")
                        break
                    else:
                        print(f"Alice: Mensagem desconhecida recebida: {data}")
                except socket.timeout:
                    print("Alice: Timeout - a sincronização falhou.")
                    break

            # Espera um breve momento antes de fechar
            time.sleep(1)
        except ConnectionRefusedError:
            print(f"Alice: Não foi possível conectar a {host}:{port}")

if __name__ == "__main__":
    alice_client()
