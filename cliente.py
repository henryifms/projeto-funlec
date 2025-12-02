import socket
import threading
import time
import ctypes
from ctypes import wintypes
import os
from datetime import datetime

SERVER_IP = "10.8.33.158"
PORT = 5000

# Arquivo de log
LOG_FILE = os.path.join(os.path.dirname(__file__), "cliente_log.txt")

def log(mensagem):
    """Escreve mensagem no arquivo de log"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensagem}\n")

BlockInput = ctypes.windll.user32.BlockInput
BlockInput.argtypes = [wintypes.BOOL]
BlockInput.restype = wintypes.BOOL

def travar_teclado_mouse():
    ok = BlockInput(True)
    if ok:
        log("Teclado/mouse BLOQUEADOS.")
        print("[CLIENTE] Teclado/mouse BLOQUEADOS.")
    else:
        log("ERRO: Não conseguiu bloquear (talvez precise rodar como ADMIN).")
        print("[CLIENTE] Não conseguiu bloquear (talvez precise rodar como ADMIN).")

def destravar_teclado_mouse():
    ok = BlockInput(False)
    if ok:
        log("Teclado/mouse DESBLOQUEADOS.")
        print("[CLIENTE] Teclado/mouse DESBLOQUEADOS.")
    else:
        log("ERRO: Não conseguiu desbloquear.")
        print("[CLIENTE] Não conseguiu desbloquear.")

def travar_por_10_segundos():
    travar_teclado_mouse()
    time.sleep(10)
    destravar_teclado_mouse()

def ouvir_servidor(sock: socket.socket):
    log("Conectado. Aguardando mensagens do servidor...")
    print("[CLIENTE] Conectado. Aguardando mensagens do servidor...")
    try:
        while True:
            dados = sock.recv(1024)
            if not dados:
                log("Servidor fechou a conexão.")
                print("[CLIENTE] Servidor fechou a conexão.")
                break

            msg = dados.decode(errors="ignore").strip()
            log(f"Mensagem recebida: {msg}")
            print(f"[SERVIDOR] {msg}")
            
            if msg.upper() == "LOCK":
                threading.Thread(target=travar_por_10_segundos, daemon=True).start()
    except Exception as e:
        log(f"ERRO ao receber dados: {e}")
        print(f"[CLIENTE] Erro ao receber dados: {e}")
    finally:
        sock.close()

def main():
    try:
        log("=== CLIENTE INICIADO ===")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_IP, PORT))
        log(f"Conectado em {SERVER_IP}:{PORT}")
        print(f"[CLIENTE] Conectado em {SERVER_IP}:{PORT}")
    except Exception as e:
        log(f"ERRO: Não conseguiu conectar: {e}")
        print(f"[CLIENTE] Não conseguiu conectar: {e}")
        return

    t = threading.Thread(target=ouvir_servidor, args=(sock,), daemon=True)
    t.start()

    print("[CLIENTE] Digite mensagens para enviar ao servidor (ou CTRL+C para sair).")
    try:
        while True:
            texto = input()
            if not texto:
                continue
            sock.sendall(texto.encode())
            log(f"Mensagem enviada: {texto}")
    except KeyboardInterrupt:
        log("Cliente finalizado pelo usuário.")
        print("\n[CLIENTE] Saindo...")
    except Exception as e:
        log(f"ERRO na thread principal: {e}")
    finally:
        sock.close()
        log("Socket fechado.")

if __name__ == "__main__":
    main()
