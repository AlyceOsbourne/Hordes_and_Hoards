import socket
from abc import ABC, abstractmethod

# this is a base definition for both the client and server
from collections import namedtuple
from threading import Thread

Address = namedtuple('Address', ['ip', 'port'])
Protocol = namedtuple('Protocol', ['header_length', 'format', 'disconnect_message'])
SocketType = namedtuple('SocketType', ['type', 'family'])
Client = namedtuple('Connection', ['connection', 'address', 'thread'])


class NetworkConnection(ABC):

    def __init__(
            self,
            address: Address,
            protocol: Protocol,
            socket_type: SocketType
    ):
        self.address = address
        self.protocol = protocol
        self.socket_type = socket_type
        self.socket = socket.socket(socket_type.family, socket_type.type)

    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def send(self, message):
        ...

    @abstractmethod
    def listen(self):
        ...

    @abstractmethod
    def disconnect(self):
        ...

    @abstractmethod
    def close(self):
        ...
