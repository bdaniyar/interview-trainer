"""Bounded Docker exec stream for the fixed in-sandbox resident module."""
import json
import socket
import struct
from time import monotonic

from sql_runner.app.config import PYTHON
from sql_runner.app.docker_backend import SandboxUnavailable
from transaction_lab.resident import WIRE_BYTES

HEADER = struct.Struct(">BxxxI")


class ResidentWire:
    def __init__(self, client, container):
        api = client.api
        exec_id = api.exec_create(container, [PYTHON, "-m", "transaction_lab.resident"],
                                  stdin=True, stdout=True, stderr=True,
                                  user="65532:65532", tty=False)["Id"]
        self.stream = api.exec_start(exec_id, socket=True, tty=False)
        self.socket = self.stream if isinstance(self.stream, socket.socket) else self.stream._sock
        self.buffer = bytearray()
        try:
            if self.read(monotonic() + 5) != {"ready": True}:
                raise SandboxUnavailable("Unexpected transaction resident handshake")
        except Exception:
            self.close()
            raise

    def close(self):
        self.socket.close()
        self.stream.close()

    def receive(self, length, deadline):
        payload = bytearray()
        while len(payload) < length:
            remaining = deadline - monotonic()
            if remaining <= 0:
                raise TimeoutError("Transaction resident deadline")
            self.socket.settimeout(remaining)
            chunk = self.socket.recv(length - len(payload))
            if not chunk:
                raise SandboxUnavailable("Transaction resident closed")
            payload.extend(chunk)
        return payload

    def read(self, deadline):
        while b"\n" not in self.buffer:
            stream, length = HEADER.unpack(self.receive(HEADER.size, deadline))
            if not 0 < length <= WIRE_BYTES or stream != 1 or len(self.buffer) + length > WIRE_BYTES + 1:
                raise SandboxUnavailable("Transaction resident output unavailable")
            self.buffer.extend(self.receive(length, deadline))
        line, _, tail = self.buffer.partition(b"\n")
        self.buffer = tail
        return json.loads(line)

    def request(self, data):
        self.socket.settimeout(2)
        self.socket.sendall(json.dumps(data, ensure_ascii=False).encode() + b"\n")
        return self.read(monotonic() + 2)
