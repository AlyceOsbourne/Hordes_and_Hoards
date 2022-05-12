import socket, threading, time, json, os, sys

HEADER = 64
HOST = socket.gethostbyname(socket.gethostname())
PORT = 25565
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(client, address):
    print("Client connected:", address)
    running = True
    while running:
        data_len = client.recv(HEADER).decode(FORMAT).strip()
        if data_len:
            data_len = int(data_len)
            msg = client.recv(data_len).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                running = False
            print(f"Received: {msg} from {address}")
            client.send(f"Received: [{msg}]".encode(FORMAT))


def start():
    server.listen()
    while True:
        threading.Thread(target=handle_client, args=server.accept()).start()


if __name__ == "__main__":
    print(f"Starting server...\nAddress: {HOST}:{PORT}")
    start()