import socket


def __init__(self, buff_size, base):
    self._buff_size = buff_size
    self._base = base
    self._socket = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
    )


def connect(self, address):
    self._socket.bind((address[0], address[1]))
