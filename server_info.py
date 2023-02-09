import socket

class ServerInfo:
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 12345
    BYTESIZE = 1024
    ENCODER = "utf-8"
    ROOMSIZE = 8
