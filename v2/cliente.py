import socket
import ctypes

UDP_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    msg = data.decode().strip()

    if msg == "LOCK_NOW":
        ctypes.windll.user32.LockWorkStation()
