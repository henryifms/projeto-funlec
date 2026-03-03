import socket
import ctypes
import jwt

SECRET = "minha_secreta"
UDP_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", UDP_PORT))

while True:
    data, addr = sock.recvfrom(4096)
    
    try:
        payload = jwt.decode(
            data.decode(),
            SECRET,
            algorithms=["HS256"]
        )

        if payload["cmd"] == "lock":
            ctypes.windll.user32.LockWorkStation()

    except jwt.ExpiredSignatureError:
        pass
    except jwt.InvalidTokenError:
        pass  
