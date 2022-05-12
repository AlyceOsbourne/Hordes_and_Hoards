import socket
import threading
import socketserver
import time
import json
from functools import partial
from lz4.block import compress, decompress

HEADER_LENGTH = 12
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '%DISCONNECT%'


class _Handler(socketserver.BaseRequestHandler):
    def handle(self):
        print(f"{self.client_address[0]}:{self.client_address[1]} connected")
        while True:
            try:
                message_len = int(self.request.recv(HEADER_LENGTH).decode(FORMAT))
                message = decompress(self.request.recv(message_len)).decode(FORMAT)
                if message == DISCONNECT_MESSAGE:
                    self.disconnect()
                else:
                    self.handle_message(message)
            except Exception as e:
                print(f"{self.client_address[0]}:{self.client_address[1]} disconnected")
                break

    def send_message(self, message):
        message = compress(json.dumps(message).encode(FORMAT))
        message_len = len(message)
        self.request.send(f"{message_len:<{HEADER_LENGTH}}".encode(FORMAT))
        self.request.send(message)

    def disconnect(self):
        self.send_message(DISCONNECT_MESSAGE)
        self.request.close()

    def handle_message(self, message):
        print(f"{self.client_address[0]}:{self.client_address[1]} sent {message}")


class _Client:
    def __init__(self, address, message_handler):
        self.host, self.port = address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_handler = message_handler

    def send_message(self, message: str):
        message = compress(json.dumps(message).encode(FORMAT))
        message_len = len(message)
        self.socket.send(f"{message_len:<{HEADER_LENGTH}}".encode(FORMAT))
        self.socket.send(message)

    def receive_message(self):
        message_len = self.socket.recv(HEADER_LENGTH).decode(FORMAT)
        if message_len:
            message_len = int(message_len)
            message = decompress(self.socket.recv(message_len)).decode(FORMAT)
            if message:
                return json.loads(message)

    def disconnect(self):
        self.socket.close()

    def run(self):
        self.socket.connect((self.host, self.port))
        while True:
            message = self.receive_message()
            if message:
                self.handle_message(message)
            time.sleep(0.1)

    def handle_message(self, message):
        if message == DISCONNECT_MESSAGE:
            self.disconnect()
        else:
            self.message_handler(message)


def init():
    ADDR = (socket.gethostbyname(socket.gethostname()), 9090)
    server = socketserver.TCPServer(ADDR, _Handler)
    client = _Client(ADDR, print)
    server_thread = threading.Thread(target=server.serve_forever)
    client_thread = threading.Thread(target=client.run)
    server_thread.start()
    client_thread.start()
    return client, server


if __name__ == '__main__':
    client, server = init()
    time.sleep(0.5)
    while (msg := input(">>> ")) != 'q':
        client.send_message(msg)
        time.sleep(0.5)
    client.disconnect()
