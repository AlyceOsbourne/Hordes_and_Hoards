import socket

HEADER = 64
PORT = 25565
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = socket.gethostbyname(socket.gethostname())

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((SERVER, PORT))


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = f"{len(message):<{HEADER}}".encode(FORMAT)
    socket.send(msg_length)
    socket.send(message)


def receive():
    msg_length = socket.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        return socket.recv(msg_length).decode(FORMAT)
    else:
        return None


while True:
    if (msg := input('> ')) != 'q':
        send(msg)
