import socket
import threading
import socketserver
import time
import json
from abc import abstractmethod, ABCMeta

from lz4.block import compress, decompress

HEADER_LENGTH = 12
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '%DISCONNECT%'


class _Handler(socketserver.BaseRequestHandler, metaclass=ABCMeta):
    def handle(self):
        while True:
            try:
                message_len = int(self.request.recv(HEADER_LENGTH).decode(FORMAT))
                message = decompress(self.request.recv(message_len)).decode(FORMAT)
                if message == DISCONNECT_MESSAGE:
                    self.disconnect()
                else:
                    self.handle_message(message)
            except socket.error:
                break

    def send_message(self, message):
        message = compress(json.dumps(message).encode(FORMAT))
        message_len = len(message)
        self.request.send(f"{message_len:<{HEADER_LENGTH}}".encode(FORMAT))
        self.request.send(message)

    def disconnect(self):
        self.send_message(DISCONNECT_MESSAGE)
        self.request.close()

    @abstractmethod
    def handle_message(self, message):
        ...


class _Client(metaclass=ABCMeta):
    def __init__(self, address):
        self.host, self.port = address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
                message = json.loads(message)
                if message == DISCONNECT_MESSAGE:
                    self.disconnect()
                else:
                    self.handle_message(message)

    def disconnect(self):
        self.socket.close()


    def run(self):
        self.socket.connect((self.host, self.port))
        while True:
            self.receive_message()


    @abstractmethod
    def handle_message(self, message):
        ...


def init():
    ADDR = (socket.gethostbyname(socket.gethostname()), 9090)
    server = socketserver.TCPServer(ADDR, _Handler)
    client = _Client(ADDR)
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
