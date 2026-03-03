import socket
import ctypes
import subprocess

UDP_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", UDP_PORT))

print("Escutando comandos...")

while True:
    data, addr = sock.recvfrom(1024)
    msg = data.decode().strip().upper()

    if msg == "LOCK":
        print("Bloqueando sessão...")
        ctypes.windll.user32.LockWorkStation()

    elif msg == "SHUTDOWN":
        print("Desligando em 5 segundos...")
        subprocess.run(["shutdown", "/s", "/t", "5", "/f"], check=False)
