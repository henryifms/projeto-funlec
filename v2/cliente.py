import socket
import ctypes
from ctypes import wintypes
import threading
import time

UDP_PORT = 9999
is_blocked = False  # Estado global do bloqueio

# BlockInput
BlockInput = ctypes.windll.user32.BlockInput
BlockInput.argtypes = [wintypes.BOOL]
BlockInput.restype = wintypes.BOOL

def toggle_input_block():
    global is_blocked
    
    is_blocked = not is_blocked
    success = BlockInput(is_blocked)
    
    status = "BLOQUEADO" if is_blocked else "LIBERADO"
    
    if success:
        print(f"Teclado/Mpuse: {status}")
    else:
        print(f"FALHa ao {status.lower()} (Execute como ADMIN!)")
    
    return success

# Socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", UDP_PORT))

print("Escutando comandos UDP na porta 9999..")
print("Execute como ADMINISTRADOR PARA bloquear teclado!")
print("Comandos: LOCK_SESSION | TOGGLE_INPUT")
print("-" * 50)

try:
    while True:
        data, addr = sock.recvfrom(1024)
        msg = data.decode().strip().upper()
        print(f"Recebido d {addr}: {msg}")
        
        if msg == "LOCK_SESSION":
            print("Bloqueando sessão (Windows+L)...")
            ctypes.windll.user32.LockWorkStation()
            
        elif msg == "TOGGLE_INPUT":
            # Executa em thread separada para não travar o socket
            threading.Thread(target=toggle_input_block, daemon=True).start()
            
except KeyboardInterrupt:
    print("\nSaindo...")
finally:
    sock.close()
