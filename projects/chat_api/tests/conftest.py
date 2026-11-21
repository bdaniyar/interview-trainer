import socket

import pytest


@pytest.fixture(autouse=True)
def deny_network(monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError("offline contract suite attempted a network connection")

    monkeypatch.setattr(socket.socket, "connect", fail)
    monkeypatch.setattr(socket.socket, "connect_ex", fail)
    monkeypatch.setattr(socket, "create_connection", fail)
    monkeypatch.setattr(socket, "getaddrinfo", fail)
