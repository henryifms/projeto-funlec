import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clientes = []
lock_clientes = threading.Lock()

def tratar_cliente(conn, addr):
    print(f"[+] Novo cliente conectado: {addr}")
    with lock_clientes:
        clientes.append(conn)
    try:
        while True:
            dados = conn.recv(1024)
            if not dados:
                break
            print(f"[CLIENTE {addr}] {dados.decode(errors='ignore').strip()}")
    except Exception as e:
        print(f"[!] Erro com cliente {addr}: {e}")
    finally:
        print(f"[-] Cliente desconectado: {addr}")
        with lock_clientes:
            if conn in clientes:
                clientes.remove(conn)
        conn.close()

def aceitar_conexoes():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"[SERVIDOR] Escutando em {HOST}:{PORT}")

    while True:
        conn, addr = servidor.accept()
        thread = threading.Thread(target=tratar_cliente, args=(conn, addr), daemon=True)
        thread.start()

def enviar_para_todos(mensagem: str):
    dados = mensagem.encode()
    with lock_clientes:
        for c in list(clientes):
            try:
                c.sendall(dados)
            except Exception as e:
                print(f"[!] Erro ao enviar para um cliente: {e}")
                clientes.remove(c)
                c.close()

def main():
    thread_accept = threading.Thread(target=aceitar_conexoes, daemon=True)
    thread_accept.start()

    print("[SERVIDOR] Simulando Arduino.")
    print("[SERVIDOR] Quando voce apertar ENTER, vou mandar LOCK para todos os clientes.")

    while True:
        _ = input()  # como se fosse o botão
        print("[SERVIDOR] BOTAO_SOLTO_EXECUTAR (simulado)")
        enviar_para_todos("LOCK")

if __name__ == "__main__":
    main()
