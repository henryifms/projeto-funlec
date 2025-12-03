import socket
import threading
import time

HOST = "0.0.0.0"
PORT = 5000

clientes = []
lock_clientes = threading.Lock()

RECONECTAR_DELAY = 5

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
    """
    Função que tenta aceitar conexões com retry automático.
    Se der erro, espera RECONECTAR_DELAY e tenta novamente.
    """
    tentativa = 1
    while True:
        try:
            print(f"\n[SERVIDOR] Tentativa {tentativa} de abrir socket...")
            servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor.bind((HOST, PORT))
            servidor.listen()
            print(f"[SERVIDOR] Escutando em {HOST}:{PORT}")
            
            tentativa = 1  # Reset tentativas após sucesso
            
            while True:
                conn, addr = servidor.accept()
                thread = threading.Thread(target=tratar_cliente, args=(conn, addr), daemon=True)
                thread.start()
        except Exception as e:
            print(f"[!] ERRO no socket servidor (Tentativa {tentativa}): {e}")
            print(f"[SERVIDOR] Reententar em {RECONECTAR_DELAY}s...")
            time.sleep(RECONECTAR_DELAY)
            tentativa += 1

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
    print("[SERVIDOR] ESPACO = desligar PCs, ENTER = LOCK, CTRL+C = sair.")

    try:
        while True:
            tecla = input()  # aqui continua sendo ENTER, vamos usar só ENTER por simplicidade
            if tecla.strip() == "":
                # ENTER: ainda manda LOCK se quiser manter a função antiga
                print("[SERVIDOR] BOTAO_SOLTO_EXECUTAR (simulado) -> LOCK")
                enviar_para_todos("LOCK")
            elif tecla.strip().upper() == "S":
                # Se digitar S e ENTER, manda SHUTDOWN
                print("[SERVIDOR] Enviando SHUTDOWN para todos os clientes...")
                enviar_para_todos("SHUTDOWN")
    except KeyboardInterrupt:
        print("\n[SERVIDOR] Encerrando por CTRL+C...")

if __name__ == "__main__":
    main()
