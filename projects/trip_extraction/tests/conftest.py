import socket

import pytest


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    attempts = []

    def blocked(*args, **kwargs):
        attempts.append(True)
        raise AssertionError("offline test attempted a network connection")

    monkeypatch.setattr(socket.socket, "connect", blocked)
    monkeypatch.setattr(socket.socket, "connect_ex", blocked)
    monkeypatch.setattr(socket, "create_connection", blocked)
    monkeypatch.setattr(socket, "getaddrinfo", blocked)

    yield
    assert not attempts, "offline test attempted a network connection"
