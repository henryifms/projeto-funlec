import socket
import threading
import time
import ctypes
from ctypes import wintypes
import os
from datetime import datetime

# Configurações do servidor
SERVER_IP = "10.8.33.158"  # IP do servidor
PORT = 5000                # Porta do servidor

# Arquivo de log
LOG_FILE = os.path.join(os.path.dirname(__file__), "cliente_log.txt")

def log(mensagem):
    """Escreve mensagem no arquivo de log"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensagem}\n")

# Funções para bloquear/desbloquear teclado e mouse
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

def conectar_ao_servidor():
    """Tenta conectar ao servidor, retornando o socket conectado ou None"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_IP, PORT))
        log(f"Conectado em {SERVER_IP}:{PORT}")
        print(f"[CLIENTE] Conectado em {SERVER_IP}:{PORT}")
        return sock
    except Exception as e:
        log(f"Erro ao conectar: {e}")
        print(f"[CLIENTE] Erro ao conectar: {e}")
        sock.close()
        return None

def main():
    while True:
        sock = conectar_ao_servidor()
        if sock:
            # Se conseguiu conectar, inicia a thread de escuta
            t = threading.Thread(target=ouvir_servidor, args=(sock,), daemon=True)
            t.start()

            print("[CLIENTE] Digite mensagens para enviar ao servidor (ou CTRL+C para sair).")
            try:
                while True:
                    texto = input()
                    if not texto:
                        continue
                    sock.sendall(texto.encode())
                # Se o input terminar (CTRL+C), sai do loop
            except KeyboardInterrupt:
                log("Cliente finalizado pelo usuário.")
                print("\n[CLIENTE] Saindo...")
                sock.close()
                break
            except Exception as e:
                log(f"Erro na comunicação: {e}")
                sock.close()
                # Tenta reconectar após um tempo
                print("[CLIENTE] Reconectando em 5 segundos...")
                time.sleep(5)
        else:
            # Se não conseguiu conectar, espera antes de tentar novamente
            print("[CLIENTE] Tentando reconectar em 5 segundos...")
            time.sleep(5)

if __name__ == "__main__":
    main()
