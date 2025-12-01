import socket
import threading
import time
import ctypes
from ctypes import wintypes

SERVER_IP = "127.0.0.1"  # troque pelo IP do servidor na rede, se não for na mesma máquina
PORT = 5000

# Função do Windows para bloquear entrada
BlockInput = ctypes.windll.user32.BlockInput
BlockInput.argtypes = [wintypes.BOOL]
BlockInput.restype = wintypes.BOOL

def travar_teclado_mouse():
    ok = BlockInput(True)
    if ok:
        print("[CLIENTE] Teclado/mouse BLOQUEADOS.")
    else:
        print("[CLIENTE] Não conseguiu bloquear (talvez precise rodar como ADMIN).")

def destravar_teclado_mouse():
    ok = BlockInput(False)
    if ok:
        print("[CLIENTE] Teclado/mouse DESBLOQUEADOS.")
    else:
        print("[CLIENTE] Não conseguiu desbloquear.")

def travar_por_10_segundos():
    travar_teclado_mouse()
    time.sleep(10)
    destravar_teclado_mouse()

def ouvir_servidor(sock: socket.socket):
    print("[CLIENTE] Conectado. Aguardando mensagens do servidor...")
    try:
        while True:
            dados = sock.recv(1024)
            if not dados:
                print("[CLIENTE] Servidor fechou a conexão.")
                break
            msg = dados.decode(errors="ignore").strip()
            print(f"[SERVIDOR] {msg}")

            if msg.upper() == "LOCK":
                # roda em uma thread separada para não travar o recebimento
                threading.Thread(target=travar_por_10_segundos, daemon=True).start()

    except Exception as e:
        print(f"[CLIENTE] Erro ao receber dados: {e}")
    finally:
        sock.close()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_IP, PORT))
        print(f"[CLIENTE] Conectado em {SERVER_IP}:{PORT}")
    except Exception as e:
        print(f"[CLIENTE] Não conseguiu conectar: {e}")
        return

    # thread para ficar ouvindo o servidor
    t = threading.Thread(target=ouvir_servidor, args=(sock,), daemon=True)
    t.start()

    print("[CLIENTE] Digite mensagens para enviar ao servidor (ou CTRL+C para sair).")
    try:
        while True:
            texto = input()
            if not texto:
                continue
            sock.sendall(texto.encode())
    except KeyboardInterrupt:
        print("\n[CLIENTE] Saindo...")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
